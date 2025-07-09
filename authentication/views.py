from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.sessions.models import Session
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from utils.database import execute_query, fetch_one
from utils.authentication import require_authentication, allow_any
import uuid
from datetime import datetime, date

@ensure_csrf_cookie
@api_view(['GET'])
@allow_any
def get_csrf_token(request):
    """Get CSRF token for frontend authentication"""
    return Response({'csrfToken': request.META.get('CSRF_COOKIE')})

@api_view(['POST'])
@allow_any
def login_user(request):
    """
    Feature 2: Login functionality
    POST /api/auth/login/
    """
    try:
        data = request.data
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return Response({
                'error': 'Email dan password harus diisi'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if user exists in AKUN table
        user_query = """
            SELECT email, password, nama, is_verified, kota_asal, gender, 
                   tempat_lahir, tanggal_lahir
            FROM AKUN 
            WHERE email = %s AND password = %s
        """
        user = fetch_one(user_query, [email, password])
        
        if not user:
            # Check if it's a label
            label_query = """
                SELECT email, password, nama, kontak
                FROM LABEL 
                WHERE email = %s AND password = %s
            """
            label = fetch_one(label_query, [email, password])
            
            if not label:
                return Response({
                    'error': 'Email atau password salah'
                }, status=status.HTTP_401_UNAUTHORIZED)
            
            # Label login
            request.session['user_email'] = label['email']
            request.session['user_type'] = 'label'
            request.session['user_name'] = label['nama']
            
            return Response({
                'message': 'Login berhasil',
                'user': {
                    'email': label['email'],
                    'nama': label['nama'],
                    'is_label': True,
                    'is_artist': False,
                    'is_songwriter': False,
                    'is_podcaster': False,
                    'is_premium': False,
                    'kontak': label['kontak']
                }
            })
        
        # User login - determine roles
        roles = []
        
        # Check if user is Artist
        artist_query = "SELECT id FROM ARTIST WHERE email_akun = %s"
        if fetch_one(artist_query, [email]):
            roles.append('artist')
        
        # Check if user is Songwriter
        songwriter_query = "SELECT id FROM SONGWRITER WHERE email_akun = %s"
        if fetch_one(songwriter_query, [email]):
            roles.append('songwriter')
        
        # Check if user is Podcaster
        podcaster_query = "SELECT email FROM PODCASTER WHERE email = %s"
        if fetch_one(podcaster_query, [email]):
            roles.append('podcaster')
        
        # Default role is 'user' if no specific roles
        if not roles:
            roles = ['user']
        
        # Check premium status
        premium_query = "SELECT email FROM PREMIUM WHERE email = %s"
        is_premium = bool(fetch_one(premium_query, [email]))
        
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
    """
    Feature 2: Logout functionality
    POST /api/auth/logout/
    """
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
    """
    Get current user information
    GET /api/auth/me/
    """
    try:
        user_email = request.user_email
        user_roles = request.user_roles
        is_premium = request.is_premium
        
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
                'user': {
                    'email': label['email'],
                    'nama': label['nama'],
                    'is_label': True,
                    'is_artist': False,
                    'is_songwriter': False,
                    'is_podcaster': False,
                    'is_premium': False,
                    'kontak': label['kontak']
                }
            })
        
        # Regular user
        user_query = """
            SELECT email, nama, is_verified, kota_asal, gender, 
                   tempat_lahir, tanggal_lahir
            FROM AKUN 
            WHERE email = %s
        """
        user = fetch_one(user_query, [user_email])
        
        if not user:
            return Response({
                'error': 'User tidak ditemukan'
            }, status=status.HTTP_404_NOT_FOUND)
        
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
    """
    Feature 3: User Registration
    POST /api/auth/register/user/
    """
    try:
        data = request.data
        
        # Required fields
        email = data.get('email')
        password = data.get('password')
        nama = data.get('nama')
        gender = data.get('gender')
        tempat_lahir = data.get('tempat_lahir')
        tanggal_lahir = data.get('tanggal_lahir')
        kota_asal = data.get('kota_asal')
        roles = data.get('roles', [])
        
        # Validation
        if not all([email, password, nama, gender is not None, tempat_lahir, tanggal_lahir, kota_asal]):
            return Response({
                'error': 'Semua field wajib diisi'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if email already exists
        check_user_query = "SELECT email FROM AKUN WHERE email = %s"
        existing_user = fetch_one(check_user_query, [email])
        
        if existing_user:
            return Response({
                'error': 'Email sudah terdaftar'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        check_label_query = "SELECT email FROM LABEL WHERE email = %s"
        existing_label = fetch_one(check_label_query, [email])
        
        if existing_label:
            return Response({
                'error': 'Email sudah terdaftar sebagai label'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        is_verified = len(roles) > 0
        
        # Insert into AKUN table
        insert_user_query = """
            INSERT INTO AKUN (email, password, nama, gender, tempat_lahir, tanggal_lahir, kota_asal, is_verified)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        execute_query(insert_user_query, [
            email, password, nama, gender, tempat_lahir, 
            tanggal_lahir, kota_asal, is_verified
        ])
        
        # Handle roles
        if 'artist' in roles:
            # Create copyright owner first
            copyright_id = str(uuid.uuid4())
            execute_query("INSERT INTO PEMILIK_HAK_CIPTA (id, rate_royalti) VALUES (%s, %s)", [copyright_id, 50])
            
            artist_id = str(uuid.uuid4())
            insert_artist_query = "INSERT INTO ARTIST (id, email_akun, id_pemilik_hak_cipta) VALUES (%s, %s, %s)"
            execute_query(insert_artist_query, [artist_id, email, copyright_id])
        
        if 'songwriter' in roles:
            # Create copyright owner first
            copyright_id = str(uuid.uuid4())
            execute_query("INSERT INTO PEMILIK_HAK_CIPTA (id, rate_royalti) VALUES (%s, %s)", [copyright_id, 50])
            
            songwriter_id = str(uuid.uuid4())
            insert_songwriter_query = "INSERT INTO SONGWRITER (id, email_akun, id_pemilik_hak_cipta) VALUES (%s, %s, %s)"
            execute_query(insert_songwriter_query, [songwriter_id, email, copyright_id])
        
        if 'podcaster' in roles:
            insert_podcaster_query = "INSERT INTO PODCASTER (email) VALUES (%s)"
            execute_query(insert_podcaster_query, [email])
        
        return Response({
            'message': 'Registrasi berhasil'
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({
            'error': f'Terjadi kesalahan: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@allow_any
def register_label(request):
    """
    Feature 3: Label Registration
    POST /api/auth/register/label/
    """
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