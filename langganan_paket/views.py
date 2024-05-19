import datetime
import uuid
from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone

def langganan_paket(request):
    # Buat user_id unik jika belum ada dalam sesi
    if 'user_id' not in request.session:
        request.session['user_id'] = str(uuid.uuid4())
    return render(request, 'langganan_paket.html')

def pembayaran_paket(request):
    if request.method == 'POST':
        # Mendapatkan jenis paket dan harga dari parameter POST
        jenis_paket = request.POST.get('jenis')
        harga = request.POST.get('harga')
        metode_pembayaran = request.POST.get('metode_pembayaran')
        user_id = request.session.get('user_id')  # Mendapatkan user_id dari session

        # Debugging: Cetak nilai yang diterima dari form
        print("Jenis Paket:", jenis_paket)
        print("Harga:", harga)
        print("Metode Pembayaran:", metode_pembayaran)
        print("User ID:", user_id)

        if not jenis_paket or not harga or not metode_pembayaran:
            return HttpResponseBadRequest("Missing parameters")

        # Mengambil tanggal sekarang
        tanggal_sekarang = timezone.now().date()

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
            return HttpResponseBadRequest("Jenis paket tidak valid")

        # Simpan informasi transaksi dalam session
        transaksi = {
            'jenis': jenis_paket,
            'tanggal_dimulai': tanggal_sekarang.strftime("%Y-%m-%d"),
            'tanggal_berakhir': tanggal_berakhir.strftime("%Y-%m-%d"),
            'metode_pembayaran': metode_pembayaran,
            'nominal': harga,
            'user_id': user_id
        }
        
        # Cek apakah sudah ada riwayat transaksi dalam session
        if 'riwayat_transaksi' not in request.session:
            request.session['riwayat_transaksi'] = []
        
        # Tambahkan informasi transaksi ke dalam riwayat transaksi dalam session
        request.session['riwayat_transaksi'].append(transaksi)
        request.session.modified = True
        
        # Ubah status langganan pengguna menjadi "Premium"
        request.session["is_premium"] = True
        
        # Tampilkan pesan sukses
        messages.success(request, 'Pembayaran berhasil! Akun Anda sekarang telah menjadi Premium.')
        
        # Redirect ke halaman riwayat transaksi
        return redirect('langganan_paket:riwayat_transaksi')
    else:
        # Jika bukan metode POST, kembalikan halaman pembayaran
        return render(request, 'pembayaran_paket.html')

def riwayat_transaksi(request):
    user_id = request.session.get('user_id')  # Mendapatkan user_id dari session
    riwayat_transaksi = request.session.get('riwayat_transaksi', [])
    
    # Filter transaksi yang hanya terkait dengan user_id
    user_transaksi = [transaksi for transaksi in riwayat_transaksi if transaksi.get('user_id') == user_id]

    # Debugging: Cetak riwayat transaksi yang diambil dari session
    print("Riwayat Transaksi:", user_transaksi)

    return render(request, 'riwayat_transaksi.html', {'riwayat_transaksi': user_transaksi})