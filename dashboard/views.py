from django.shortcuts import render

def dashboard_pengguna_biasa(request):
    dummy_pengguna_biasa = {
        "registered_as": "pengguna",
        "nama": "Muhammad Hilal Darul Fauzan",
        "email": "hilalfauzan9@gmail.com",
        "kota_asal": "Jakarta",
        "gender": "Laki-laki",
        "tempat_lahir": "California",
        "tanggal_lahir": "27 April 2004",
        "role": "Pengguna Biasa"
    }

    return render(request, 'pengguna/dashboard_pengguna_biasa.html', dummy_pengguna_biasa)

def dashboard_artist_songwriter(request):
    dummy_artist_songwriter = {
        "registered_as": "pengguna",
        "nama": "Kelly Walsh",
        "email": "barbaragreen@yahoo.com",
        "kota_asal": "Michaelstad",
        "gender": "Perempuan",
        "tempat_lahir": "Jonesbury",
        "tanggal_lahir": "21 September 1988",
        "role": "Artist/Songwriter"
    }

    return render(request, 'pengguna/dashboard_artist_songwriter.html', dummy_artist_songwriter)

def dashboard_podcaster(request):
    dummy_podcaster = {
        "registered_as": "pengguna",
        "nama": "Beth White",
        "email": "hilljason@gmail.com",
        "kota_asal": "Port Bradleyburgh",
        "gender": "Laki-laki",
        "tempat_lahir": "Ryanmouth",
        "tanggal_lahir": "14 July 2000",
        "role": "Podcaster"
    }

    return render(request, 'pengguna/dashboard_podcaster.html', dummy_podcaster)

def dashboard_label(request):
    dummy_label = {
        "registered_as": "label",
        "nama": "Singleton, Welch and Rios",
        "email": "derek22@hotmail.com",
        "kontak": "7185100571",
    }

    return render(request, 'label/dashboard_label.html', dummy_label)