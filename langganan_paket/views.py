from django.shortcuts import render

def langganan_paket(request):
    return render(request, 'langganan_paket.html')

def pembayaran_paket(request):
    return render(request, 'pembayaran_paket.html')

def riwayat_transaksi(request):
    return render(request, 'riwayat_transaksi.html')
