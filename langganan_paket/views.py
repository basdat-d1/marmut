from datetime import datetime, timedelta
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from utils.database import execute_query, execute_single_query, execute_insert_query, execute_update_query, execute_delete_query, fetch_one, fetch_all
import uuid
from utils.authentication import require_authentication

@api_view(['GET'])
@require_authentication
def get_packages(request):
    """
    Feature 7: Get all available subscription packages
    GET /api/subscription/packages/
    """
    try:
        packages_query = """
            SELECT jenis, harga
            FROM PAKET
            ORDER BY 
                CASE 
                    WHEN jenis = '1 Bulan' THEN 1
                    WHEN jenis = '3 Bulan' THEN 2
                    WHEN jenis = '6 Bulan' THEN 3
                    WHEN jenis = '1 Tahun' THEN 4
                    ELSE 5
                END
        """
        packages = fetch_all(packages_query)
        
        package_data = []
        for package in packages:
            package_data.append({
                'jenis': package['jenis'],
                'harga': package['harga'],
                'harga_formatted': f"Rp{package['harga']:,}".replace(',', '.')
            })
        
        return Response({
            'packages': package_data,
            'total': len(package_data)
        })
        
    except Exception as e:
        return Response({
            'error': f'Terjadi kesalahan: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@require_authentication
def get_user_subscription(request):
    """
    Feature 7: Get user's current subscription
    GET /api/subscription/
    """
    try:
        email = request.user_email
        if not email:
            return Response({'error': 'Not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Check if user is premium
        is_premium = fetch_one(
            "SELECT email FROM PREMIUM WHERE email = %s",
            [email]
        )
        
        if not is_premium:
            return Response({
                'is_premium': False,
                'subscription': None
            }, status=status.HTTP_200_OK)
        
        # Get current active subscription
        current_subscription = fetch_one(
            """SELECT t.jenis_paket, t.nominal, t.timestamp_dimulai, t.timestamp_berakhir, t.metode_bayar
               FROM TRANSACTION t
               WHERE t.email = %s AND t.timestamp_berakhir > NOW()
               ORDER BY t.timestamp_berakhir DESC
               LIMIT 1""",
            [email]
        )
        
        if current_subscription:
            return Response({
                'is_premium': True,
                'subscription': {
                    'jenis': current_subscription['jenis_paket'],
                    'jenis_paket': current_subscription['jenis_paket'],
                    'harga': current_subscription['nominal'],
                    'nominal': current_subscription['nominal'],
                    'timestamp_dimulai': current_subscription['timestamp_dimulai'].strftime('%d %B %Y, %H:%M'),
                    'timestamp_berakhir': current_subscription['timestamp_berakhir'].strftime('%d %B %Y, %H:%M'),
                    'metode_bayar': current_subscription['metode_bayar']
                }
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'is_premium': False,
                'subscription': None
            }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@require_authentication
def subscribe_package(request):
    """
    Feature 7: Subscribe to a package
    POST /api/subscription/subscribe/
    """
    try:
        user_email = request.user_email
        data = request.data
        
        jenis_paket = data.get('jenis_paket')
        metode_bayar = data.get('metode_bayar')
        
        if not jenis_paket or not metode_bayar:
            return Response({
                'error': 'Jenis paket dan metode pembayaran harus diisi'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if package exists
        package_query = "SELECT jenis, harga FROM PAKET WHERE jenis = %s"
        package = fetch_one(package_query, [jenis_paket])
        
        if not package:
            return Response({
                'error': 'Paket tidak ditemukan'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Check if user has active subscription
        active_subscription_query = """
            SELECT timestamp_berakhir FROM TRANSACTION 
            WHERE email = %s AND timestamp_berakhir > NOW()
            ORDER BY timestamp_berakhir DESC LIMIT 1
        """
        active_subscription = fetch_one(active_subscription_query, [user_email])
        
        if active_subscription:
            # User already has active subscription - return user-friendly error
            return Response({
                'error': 'Anda sudah memiliki langganan aktif. Langganan akan berakhir pada ' + 
                        active_subscription['timestamp_berakhir'].strftime('%d %B %Y, %H:%M') + 
                        '. Silakan tunggu hingga berakhir untuk berlangganan kembali.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Calculate subscription period based on package type
        now = datetime.now()
        if jenis_paket == '1 Bulan':
            duration_days = 30
        elif jenis_paket == '3 Bulan':
            duration_days = 90
        elif jenis_paket == '6 Bulan':
            duration_days = 180
        elif jenis_paket == '1 Tahun':
            duration_days = 365
        else:
            return Response({
                'error': 'Jenis paket tidak valid'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        start_date = now
        end_date = now + timedelta(days=duration_days)
        
        try:
            # Create transaction - trigger will automatically move user from NONPREMIUM to PREMIUM
            transaction_id = str(uuid.uuid4())
            insert_transaction_query = """
                INSERT INTO TRANSACTION (id, jenis_paket, email, timestamp_dimulai, 
                                       timestamp_berakhir, metode_bayar, nominal)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            execute_query(insert_transaction_query, [
                transaction_id, jenis_paket, user_email, start_date, end_date, 
                metode_bayar, package['harga']
            ], fetch=False)
            
            # Update session to reflect premium status (verify from database)
            premium_check = fetch_one("SELECT email FROM PREMIUM WHERE email = %s", [user_email])
            if premium_check:
                request.session['is_premium'] = True
                # Also update the request object for immediate use
                request.is_premium = True
                
                # Save session explicitly
                request.session.save()

            return Response({
                'message': 'Berlangganan berhasil!',
                'transaction': {
                    'id': transaction_id,
                    'jenis_paket': jenis_paket,
                    'harga': package['harga'],
                    'metode_bayar': metode_bayar,
                    'tanggal_dimulai': start_date.isoformat(),
                    'tanggal_berakhir': end_date.isoformat()
                },
                'user_premium_status': premium_check is not None
            }, status=status.HTTP_201_CREATED)
            
        except Exception as db_error:
            # Handle any unexpected database errors
            return Response({
                'error': f'Terjadi kesalahan database: {str(db_error)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    except Exception as e:
        return Response({
            'error': f'Terjadi kesalahan: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@require_authentication
def cancel_subscription(request):
    """
    Feature 7: Cancel current subscription
    POST /api/subscription/cancel/
    """
    try:
        user_email = request.user_email
        
        # Check if user has active subscription
        subscription_query = """
            SELECT id, jenis_paket, timestamp_berakhir
            FROM TRANSACTION
            WHERE email = %s AND timestamp_berakhir > NOW()
            ORDER BY timestamp_berakhir DESC
            LIMIT 1
        """
        subscription = fetch_one(subscription_query, [user_email])
        
        if not subscription:
            return Response({
                'error': 'Tidak ada langganan aktif untuk dibatalkan'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # For now, just return a message that subscription will end naturally
        # In a real system, you might want to implement immediate cancellation
        return Response({
            'message': f'Langganan {subscription["jenis_paket"]} akan berakhir pada {subscription["timestamp_berakhir"].strftime("%d %B %Y, %H:%M")}',
            'note': 'Langganan tidak akan diperpanjang otomatis'
        })
        
    except Exception as e:
        return Response({
            'error': f'Terjadi kesalahan: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@require_authentication
def get_subscription_history(request):
    """
    Feature 7: Get user's subscription history
    GET /api/subscription/history/
    """
    try:
        email = request.user_email
        if not email:
            return Response({'error': 'Not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
        
        transactions_query = """
            SELECT id, jenis_paket, timestamp_dimulai, timestamp_berakhir, 
                   metode_bayar, nominal
            FROM TRANSACTION 
            WHERE email = %s
            ORDER BY timestamp_dimulai DESC
        """
        transactions = fetch_all(transactions_query, [email])
        
        transaction_data = []
        for transaction in transactions:
            transaction_data.append({
                'id': str(transaction['id']),
                'jenis': transaction['jenis_paket'],
                'tanggal_dimulai': transaction['timestamp_dimulai'].strftime('%d %B %Y, %H:%M'),
                'tanggal_berakhir': transaction['timestamp_berakhir'].strftime('%d %B %Y, %H:%M'),
                'metode_bayar': transaction['metode_bayar'],
                'nominal': transaction['nominal'],
                'nominal_formatted': f"Rp{transaction['nominal']:,}".replace(',', '.'),
                'status': 'Aktif' if transaction['timestamp_berakhir'] > datetime.now() else 'Berakhir'
            })
        
        return Response({
            'transactions': transaction_data,
            'total': len(transaction_data)
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@require_authentication
def transaction_history(request):
    """
    Feature 7: Get user's transaction history
    GET /api/subscription/transaction-history/
    """
    try:
        user_email = request.user_email
        
        transactions_query = """
            SELECT id, jenis_paket, timestamp_dimulai, timestamp_berakhir, 
                   metode_bayar, nominal
            FROM TRANSACTION 
            WHERE email = %s
            ORDER BY timestamp_dimulai DESC
        """
        transactions = fetch_all(transactions_query, [user_email])
        
        transaction_data = []
        for transaction in transactions:
            transaction_data.append({
                'id': str(transaction['id']),
                'jenis': transaction['jenis_paket'],
                'tanggal_dimulai': transaction['timestamp_dimulai'].strftime('%d %B %Y, %H:%M'),
                'tanggal_berakhir': transaction['timestamp_berakhir'].strftime('%d %B %Y, %H:%M'),
                'metode_bayar': transaction['metode_bayar'],
                'nominal': transaction['nominal'],
                'nominal_formatted': f"Rp{transaction['nominal']:,}".replace(',', '.'),
                'status': 'Aktif' if transaction['timestamp_berakhir'] > datetime.now() else 'Berakhir'
            })
        
        return Response({
            'transactions': transaction_data,
            'total': len(transaction_data)
        })
        
    except Exception as e:
        return Response({
            'error': f'Terjadi kesalahan: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@require_authentication
def current_subscription(request):
    """
    Get current active subscription
    GET /api/subscription/current/
    """
    try:
        user_email = request.user_email
        
        # Check if user is premium
        premium_query = "SELECT email FROM PREMIUM WHERE email = %s"
        is_premium = fetch_one(premium_query, [user_email])
        
        if not is_premium:
            return Response({
                'is_premium': False,
                'message': 'User tidak memiliki langganan premium'
            })
        
        # Get current active subscription
        subscription_query = """
            SELECT jenis_paket, timestamp_dimulai, timestamp_berakhir, 
                   metode_bayar, nominal
            FROM TRANSACTION
            WHERE email = %s AND timestamp_berakhir > NOW()
            ORDER BY timestamp_berakhir DESC
            LIMIT 1
        """
        subscription = fetch_one(subscription_query, [user_email])
        
        if not subscription:
            return Response({
                'is_premium': False,
                'message': 'Tidak ada langganan aktif'
            })
        
        # Calculate days remaining
        days_remaining = (subscription['timestamp_berakhir'] - datetime.now()).days
        
        return Response({
            'is_premium': True,
            'subscription': {
                'jenis': subscription['jenis_paket'],
                'tanggal_dimulai': subscription['timestamp_dimulai'].strftime('%d %B %Y, %H:%M'),
                'tanggal_berakhir': subscription['timestamp_berakhir'].strftime('%d %B %Y, %H:%M'),
                'metode_bayar': subscription['metode_bayar'],
                'nominal': subscription['nominal'],
                'nominal_formatted': f"Rp{subscription['nominal']:,}".replace(',', '.'),
                'days_remaining': days_remaining,
                'status': 'Aktif'
            }
        })
        
    except Exception as e:
        return Response({
            'error': f'Terjadi kesalahan: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@require_authentication
def payment_methods(request):
    """
    Get available payment methods
    GET /api/subscription/payment-methods/
    """
    try:
        # Static payment methods - in real system, this might come from database
        payment_methods = [
            {
                'id': 'transfer_bank',
                'name': 'Transfer Bank',
                'description': 'Transfer melalui rekening bank'
            },
            {
                'id': 'kartu_kredit',
                'name': 'Kartu Kredit',
                'description': 'Pembayaran dengan kartu kredit'
            },
            {
                'id': 'e_wallet',
                'name': 'E-Wallet',
                'description': 'Pembayaran melalui dompet digital'
            }
        ]
        
        return Response({
            'payment_methods': payment_methods,
            'total': len(payment_methods)
        })
        
    except Exception as e:
        return Response({
            'error': f'Terjadi kesalahan: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


