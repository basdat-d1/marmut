from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from utils.database import execute_query, fetch_one
from utils.authentication import require_authentication, allow_any
import uuid
from django.db import transaction, connection

@ensure_csrf_cookie
@api_view(['GET'])
@allow_any
def get_csrf_token(request):
    """Get CSRF token for frontend authentication"""
    return Response({'csrfToken': request.META.get('CSRF_COOKIE')})

@api_view(['POST'])
@allow_any
def login_user(request):
    try:
        data = request.data
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return Response({
                'error': 'Email dan password harus diisi'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if it's a label FIRST (labels should not be in AKUN table)
        label_query = """
            SELECT email, password, nama, kontak
            FROM LABEL 
            WHERE email = %s AND password = %s
        """
        label = fetch_one(label_query, [email, password])
        
        if label:
            # Label login
            request.session['user_email'] = label['email']
            request.session['user_type'] = 'label'
            request.session['user_name'] = label['nama']
            
            return Response({
                'message': 'Login berhasil',
                'label': {
                    'email': label['email'],
                    'nama': label['nama'],
                    'kontak': label['kontak']
                }
            })
        
        # Check if user exists in AKUN table (only if not a label)
        user_query = """
            SELECT email, password, nama, is_verified, kota_asal, gender, 
                   tempat_lahir, tanggal_lahir
            FROM AKUN 
            WHERE email = %s AND password = %s
        """
        user = fetch_one(user_query, [email, password])
        
        if not user:
            return Response({
                'error': 'Email atau password salah'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        # User login
        roles_query = """
            SELECT 
                CASE WHEN a.id IS NOT NULL THEN 'artist' END as artist_role,
                CASE WHEN s.id IS NOT NULL THEN 'songwriter' END as songwriter_role,
                CASE WHEN p.email IS NOT NULL THEN 'podcaster' END as podcaster_role,
                CASE WHEN pr.email IS NOT NULL THEN true ELSE false END as is_premium
            FROM AKUN ak
            LEFT JOIN ARTIST a ON a.email_akun = ak.email
            LEFT JOIN SONGWRITER s ON s.email_akun = ak.email
            LEFT JOIN PODCASTER p ON p.email = ak.email
            LEFT JOIN PREMIUM pr ON pr.email = ak.email
            WHERE ak.email = %s
        """
        roles_result = fetch_one(roles_query, [email])
        
        # Build roles list
        roles = []
        if roles_result and roles_result['artist_role']:
            roles.append('artist')
        if roles_result and roles_result['songwriter_role']:
            roles.append('songwriter')
        if roles_result and roles_result['podcaster_role']:
            roles.append('podcaster')
        
        # Default role is 'user' if no specific roles
        if not roles:
            roles = ['user']
        
        is_premium = bool(roles_result and roles_result['is_premium'])
        
        # Store session
        request.session['user_email'] = user['email']
        request.session['user_type'] = 'user'
        request.session['user_name'] = user['nama']
        request.session['user_roles'] = roles
        request.session['is_premium'] = is_premium
        
        return Response({
            'message': 'Login berhasil',
            'user': {
                'email': user['email'],
                'nama': user['nama'],
                'is_label': False,
                'is_artist': 'artist' in roles,
                'is_songwriter': 'songwriter' in roles,
                'is_podcaster': 'podcaster' in roles,
                'is_premium': is_premium,
                'is_verified': user['is_verified'],
                'kota_asal': user['kota_asal'],
                'gender': user['gender'],
                'tempat_lahir': user['tempat_lahir'],
                'tanggal_lahir': user['tanggal_lahir'].isoformat() if user['tanggal_lahir'] else None
            }
        })
        
    except Exception as e:
        return Response({
            'error': f'Terjadi kesalahan: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@require_authentication
def logout_user(request):
    try:
        request.session.flush()
        return Response({'message': 'Logout berhasil'})
    except Exception as e:
        return Response({
            'error': f'Terjadi kesalahan: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@require_authentication
def current_user(request):
    try:
        user_email = request.user_email
        user_roles = request.user_roles
        
        # Check if user is a label
        label_query = "SELECT email FROM LABEL WHERE email = %s"
        is_label = bool(fetch_one(label_query, [user_email]))
        
        if is_label:
            label_query = """
                SELECT email, nama, kontak
                FROM LABEL 
                WHERE email = %s
            """
            label = fetch_one(label_query, [user_email])
            
            return Response({
                'label': {
                    'email': label['email'],
                    'nama': label['nama'],
                    'kontak': label['kontak']
                }
            })
        
        # Regular user
        user_query = """
            SELECT 
                ak.email, ak.nama, ak.is_verified, ak.kota_asal, ak.gender, 
                ak.tempat_lahir, ak.tanggal_lahir,
                CASE WHEN pr.email IS NOT NULL THEN true ELSE false END as is_premium
            FROM AKUN ak
            LEFT JOIN PREMIUM pr ON pr.email = ak.email
            WHERE ak.email = %s
        """
        user = fetch_one(user_query, [user_email])
        
        if not user:
            return Response({
                'error': 'User tidak ditemukan'
            }, status=status.HTTP_404_NOT_FOUND)
        
        is_premium = bool(user['is_premium'])
        
        # Sync session with database if there's a mismatch
        session_premium = request.session.get('is_premium', False)
        if is_premium != session_premium:
            request.session['is_premium'] = is_premium
            request.session.save()
                
        return Response({
            'user': {
                'email': user['email'],
                'nama': user['nama'],
                'is_label': False,
                'is_artist': 'artist' in user_roles,
                'is_songwriter': 'songwriter' in user_roles,
                'is_podcaster': 'podcaster' in user_roles,
                'is_premium': is_premium,
                'is_verified': user['is_verified'],
                'kota_asal': user['kota_asal'],
                'gender': user['gender'],
                'tempat_lahir': user['tempat_lahir'],
                'tanggal_lahir': user['tanggal_lahir'].isoformat() if user['tanggal_lahir'] else None
            }
        })
        
    except Exception as e:
        return Response({
            'error': f'Terjadi kesalahan: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@allow_any
def register_user(request):
    try:
        data = request.data
        email = data.get('email')
        password = data.get('password')
        nama = data.get('nama')
        gender = data.get('gender')
        tempat_lahir = data.get('tempat_lahir')
        tanggal_lahir = data.get('tanggal_lahir')
        kota_asal = data.get('kota_asal')
        roles = data.get('roles') or data.get('role') or []
        
        if not all([email, password, nama, gender is not None, tempat_lahir, tanggal_lahir, kota_asal]):
            return Response({'error': 'Semua field wajib diisi'}, status=status.HTTP_400_BAD_REQUEST)
        
        check_user_query = "SELECT email FROM AKUN WHERE email = %s"
        existing_user = fetch_one(check_user_query, [email])
        if existing_user:
            return Response({'error': 'Email sudah terdaftar'}, status=status.HTTP_400_BAD_REQUEST)
        
        check_label_query = "SELECT email FROM LABEL WHERE email = %s"
        existing_label = fetch_one(check_label_query, [email])
        if existing_label:
            return Response({'error': 'Email sudah terdaftar sebagai label'}, status=status.HTTP_400_BAD_REQUEST)
        
        is_verified = len(roles) > 0
        
        try:
            with transaction.atomic():
                with connection.cursor() as cursor:
                    # Insert user into AKUN table
                    # Trigger set_non_premium will automatically add user to NONPREMIUM table
                    insert_user_query = """
                        INSERT INTO AKUN (email, password, nama, gender, tempat_lahir, tanggal_lahir, kota_asal, is_verified)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    cursor.execute(insert_user_query, [
                        email, password, nama, gender, tempat_lahir, 
                        tanggal_lahir, kota_asal, is_verified
                    ])
                    
                    # Handle role-specific tables
                    if 'artist' in roles:
                        copyright_id = str(uuid.uuid4())
                        cursor.execute("INSERT INTO PEMILIK_HAK_CIPTA (id, rate_royalti) VALUES (%s, %s)", [copyright_id, 50])
                        artist_id = str(uuid.uuid4())
                        insert_artist_query = "INSERT INTO ARTIST (id, email_akun, id_pemilik_hak_cipta) VALUES (%s, %s, %s)"
                        cursor.execute(insert_artist_query, [artist_id, email, copyright_id])
                    
                    if 'songwriter' in roles:
                        copyright_id = str(uuid.uuid4())
                        cursor.execute("INSERT INTO PEMILIK_HAK_CIPTA (id, rate_royalti) VALUES (%s, %s)", [copyright_id, 50])
                        songwriter_id = str(uuid.uuid4())
                        insert_songwriter_query = "INSERT INTO SONGWRITER (id, email_akun, id_pemilik_hak_cipta) VALUES (%s, %s, %s)"
                        cursor.execute(insert_songwriter_query, [songwriter_id, email, copyright_id])
                    
                    if 'podcaster' in roles:
                        insert_podcaster_query = "INSERT INTO PODCASTER (email) VALUES (%s)"
                        cursor.execute(insert_podcaster_query, [email])
                        
            return Response({'message': 'Registrasi berhasil'}, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({'error': f'Terjadi kesalahan: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    except Exception as e:
        return Response({'error': f'Terjadi kesalahan: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@allow_any
def register_label(request):
    try:
        data = request.data
        
        # Required fields
        email = data.get('email')
        password = data.get('password')
        nama = data.get('nama')
        kontak = data.get('kontak')
        
        # Validation
        if not all([email, password, nama, kontak]):
            return Response({
                'error': 'Semua field wajib diisi'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if email already exists
        check_user_query = "SELECT email FROM AKUN WHERE email = %s"
        existing_user = fetch_one(check_user_query, [email])
        
        if existing_user:
            return Response({
                'error': 'Email sudah terdaftar sebagai user'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        check_label_query = "SELECT email FROM LABEL WHERE email = %s"
        existing_label = fetch_one(check_label_query, [email])
        
        if existing_label:
            return Response({
                'error': 'Email sudah terdaftar'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Generate label ID and copyright owner
        label_id = str(uuid.uuid4())
        copyright_id = str(uuid.uuid4())
        
        # Create copyright owner first
        execute_query("INSERT INTO PEMILIK_HAK_CIPTA (id, rate_royalti) VALUES (%s, %s)", [copyright_id, 75])
        
        # Insert into LABEL table
        insert_label_query = """
            INSERT INTO LABEL (id, nama, email, password, kontak, id_pemilik_hak_cipta)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        execute_query(insert_label_query, [label_id, nama, email, password, kontak, copyright_id])
        
        return Response({
            'message': 'Registrasi label berhasil'
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({
            'error': f'Terjadi kesalahan: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)