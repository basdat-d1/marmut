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
    
    albums = []

    if request.session.get('is_artist'):
        query =(rf"""SELECT album.id AS id_album, album.judul AS judul_album, label.nama AS label, album.jumlah_lagu AS jumlah_lagu, album.total_durasi AS total_durasi
                    FROM album
                    JOIN song ON album.id = song.id_album
                    JOIN artist ON song.id_artist = artist.id
                    JOIN akun ON artist.email_akun = akun.email
                    JOIN label ON album.id_label = label.id
                    WHERE akun.email = '{email}'
                    GROUP BY album.id, album.judul, akun.nama, label.nama, album.jumlah_lagu, album.total_durasi;
                                    """)
        cursor.execute(query)
        albums_artist = cursor.fetchall()
        for album in albums_artist:
            albums.append(album)
    elif request.session.get('is_songwriter'):
        query =(rf"""SELECT album.id AS id_album, album.judul AS judul_album, label.nama AS label, album.jumlah_lagu AS jumlah_lagu, album.total_durasi AS total_durasi
                    FROM songwriter_write_song
                    JOIN song ON songwriter_write_song.id_song = song.id_konten
                    JOIN album ON song.id_album = album.id
                    JOIN label ON album.id_label = label.id
                    JOIN songwriter ON songwriter_write_song.id_songwriter = songwriter.id
                    JOIN akun ON songwriter.email_akun = akun.email
                    WHERE songwriter.email_akun = '{email}'
                    GROUP BY album.id, album.judul, label.nama, album.jumlah_lagu, album.total_durasi;
                                    """)
        cursor.execute(query)
        albums_songwriter = cursor.fetchall()
        for album in albums_songwriter:
            albums.append(album)
    
    context = {
        "albums": albums,
        'status_langganan': request.session.get('status_langganan'),
        'isArtist': request.session.get('is_artist'),
        'isSongwriter': request.session.get('is_songwriter'),
        'isPodcaster': request.session.get('is_podcaster'),
    }

    # if request.method == 'POST':
        # email = request.POST.get('album.0')
        # password = request.POST.get('password')

        # cursor.execute("SELECT * FROM AKUN WHERE email = %s", [email])
        # user = cursor.fetchone()

        # cursor.execute("SELECT * FROM LABEL WHERE email = %s", [email])
        # label = cursor.fetchone()

        # # Kalo email atau password salah
        # if not user and not label:
        #     context["message"] = "Email atau password salah"
        #     return render(request, "login.html", context)

        # # Jika password benar
        # if user and user[1] == password:
        #     return handle_pengguna_login(cursor, request, user)
        # elif label and label[3] == password:
        #     return handle_label_login(cursor, request, label)

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

@connectdb
def list_song(cursor: CursorWrapper, request):
    id= request.GET.get("id")

    cursor.execute(rf"""SELECT judul 
                   FROM ALBUM 
                   WHERE ALBUM.id = '{id}';
                   """)
    album_judul = cursor.fetchone()

    query =(rf"""SELECT KONTEN.judul, SONG.total_play, SONG.total_download, KONTEN.durasi
                FROM KONTEN, SONG
                JOIN ALBUM ON SONG.id_album = ALBUM.id
                WHERE ALBUM.id = '{id}' AND KONTEN.id = SONG.id_konten;
                                """)
    cursor.execute(query)
    songs = cursor.fetchall()

    print(album_judul[0])
    
    context = {
        "album_judul": album_judul[0],
        "songs": songs,
        'status_langganan': request.session.get('status_langganan'),
        'isArtist': request.session.get('is_artist'),
        'isSongwriter': request.session.get('is_songwriter'),
        'isPodcaster': request.session.get('is_podcaster'),
    }

    return render(request, 'list_song_songwriter_artist.html', context)

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