from django.shortcuts import render

# Create your views here.

def list_album(request):
    dummy_album = {
        "judul": "judul 1",
        "label": "label 1",
        "jumlah_lagu": "10",
        "total_durasi": "300",
    }

    return render(request, 'list_album_songwriter_artist.html', dummy_album)

def create_album(request):

    return render(request, 'create_album_songwriter_artist.html')

def update_album(request):

    dummy_album = {
        "judul": "judul 1",
        "label": "label 1",
        "jumlah_lagu": "10",
        "total_durasi": "300",
    }

    return render(request, 'update_album_songwriter_artist.html', dummy_album)

def list_song(request):
    dummy_song = {
        "judul": "judul 1",
        "total_play": "0",
        "total_download": "10",
        "total_durasi": "300",
    }

    return render(request, 'list_song_songwriter_artist.html', dummy_song)

def create_song(request):

    return render(request, 'create_song_songwriter_artist.html')

def update_song(request):

    dummy_song = {
        "judul": "judul 1",
        "total_play": "0",
        "total_download": "10",
        "total_durasi": "300",
    }

    return render(request, 'update_song_songwriter_artist.html', dummy_song)

def list_album_label(request):
    dummy_album = {
        "judul": "judul 1",
        "label": "label 1",
        "jumlah_lagu": "10",
        "total_durasi": "300",
    }

    return render(request, 'list_album_label.html', dummy_album)

def list_song_label(request):
    dummy_song = {
        "judul": "judul 1",
        "total_play": "0",
        "total_download": "10",
        "total_durasi": "300",
    }

    return render(request, 'list_song_label.html', dummy_song)