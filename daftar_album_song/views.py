from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import redirect, render
from django.db.backends.utils import CursorWrapper
from django.http import HttpResponseRedirect
from utils.query import connectdb

# Create your views here.

@connectdb
def list_album(cursor: CursorWrapper, request):
    try:
        email = request.session.get('email')
    except:
        return HttpResponseRedirect(reverse("authentication:login_user"))
    query =(rf"""SELECT album.judul AS judul_album, label.nama AS label, album.jumlah_lagu AS jumlah_lagu, album.total_durasi AS total_durasi
                FROM album
                JOIN song ON album.id = song.id_album
                JOIN artist ON song.id_artist = artist.id
                JOIN akun ON artist.email_akun = akun.email
                JOIN label ON album.id_label = label.id
                WHERE akun.email = '{email}'
                GROUP BY album.judul, akun.nama, label.nama, album.jumlah_lagu, album.total_durasi;
                                """)
    cursor.execute(query)
    albums = cursor.fetchall()
    
    context = {
        "judul": albums[0],
        "label": albums[1],
        "jumlah_lagu": albums[2],
        "total_durasi": albums[3],
    }

    return render(request, 'list_album_songwriter_artist.html', context)

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