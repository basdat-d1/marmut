import datetime
import uuid
from django.http import HttpResponseBadRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from django.db import connection
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def langganan_paket(request):
    # Buat user_id unik jika belum ada dalam sesi
    if 'user_id' not in request.session:
        request.session['user_id'] = str(uuid.uuid4())
    return render(request, 'langganan_paket.html')

@csrf_exempt
def pembayaran_paket(request):
    if request.method == 'POST':
        # Mendapatkan jenis paket dan harga dari parameter POST
        jenis_paket = request.POST.get('jenis')
        harga = request.POST.get('harga')
        metode_pembayaran = request.POST.get('metode_pembayaran')
        
        # Mendapatkan email pengguna
        user_email = request.session.get('email')
        if not user_email:
            return HttpResponseBadRequest("Email is required")

        if not jenis_paket or not harga or not metode_pembayaran:
            return HttpResponseBadRequest("Missing parameters")

        # Mengambil tanggal sekarang
        tanggal_sekarang = timezone.now()

        # Menghitung tanggal berakhir langganan berdasarkan jenis paket yang dipilih
        if jenis_paket == '1_bulan':
            tanggal_berakhir = tanggal_sekarang + datetime.timedelta(days=30)
        elif jenis_paket == '3_bulan':
            tanggal_berakhir = tanggal_sekarang + datetime.timedelta(days=90)
        elif jenis_paket == '6_bulan':
            tanggal_berakhir = tanggal_sekarang + datetime.timedelta(days=180)
        elif jenis_paket == '1_tahun':
            tanggal_berakhir = tanggal_sekarang + datetime.timedelta(days=365)
        else:
            return HttpResponseBadRequest("Invalid package type")

        try:
            with connection.cursor() as cursor:
                # Insert paket jika belum ada
                cursor.execute("""
                    INSERT INTO PAKET (jenis, harga) 
                    VALUES (%s, %s) 
                    ON CONFLICT (jenis) DO NOTHING
                """, [jenis_paket, harga])

                # Insert transaksi
                transaksi_id = uuid.uuid4()
                cursor.execute("""
                    INSERT INTO TRANSACTION (id, jenis_paket, email, timestamp_dimulai, timestamp_berakhir, metode_bayar, nominal) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, [
                    transaksi_id, jenis_paket, user_email, 
                    tanggal_sekarang, tanggal_berakhir, 
                    metode_pembayaran, harga
                ])

                # Ubah status langganan pengguna menjadi "Premium" (masukkan ke tabel PREMIUM)
                cursor.execute("""
                    INSERT INTO PREMIUM (email) 
                    VALUES (%s) 
                    ON CONFLICT (email) DO NOTHING
                """, [user_email])

                # Set session is_premium menjadi True
                request.session['is_premium'] = True

            # Tampilkan pesan sukses
            messages.success(request, 'Pembayaran berhasil! Akun Anda sekarang telah menjadi Premium.')

        except Exception as e:
            print("Error saving transaction:", e)
            messages.error(request, 'Terjadi kesalahan dalam proses pembayaran.')

        # Redirect ke halaman riwayat transaksi dengan namespace 'langganan_paket'
        return redirect('langganan_paket:riwayat_transaksi')
    else:
        # Jika bukan metode POST, kembalikan halaman pembayaran
        return render(request, 'pembayaran_paket.html')

@csrf_exempt
def riwayat_transaksi(request):
    user_email = request.session.get('email')  # Mendapatkan email pengguna dari session

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, jenis_paket, timestamp_dimulai, timestamp_berakhir, metode_bayar, nominal 
            FROM TRANSACTION 
            WHERE email = %s
        """, [user_email])
        transaksi_list = cursor.fetchall()

    # Debugging: Cetak riwayat transaksi yang diambil dari basis data
    print("Riwayat Transaksi:", transaksi_list)

    return render(request, 'riwayat_transaksi.html', {'riwayat_transaksi': transaksi_list})
