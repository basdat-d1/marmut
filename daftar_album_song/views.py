from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import redirect, render
from django.db.backends.utils import CursorWrapper
from django.http import HttpResponseRedirect
from utils.query import connectdb
import uuid
import random
import datetime

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

    return render(request, 'list_album_songwriter_artist.html', context)

@connectdb
def create_album(cursor: CursorWrapper, request):

    # id= request.GET.get("id")

    try:
        email = request.session.get('email')
    except:
        return HttpResponseRedirect(reverse("authentication:login_user"))

    if request.method == 'POST':
        judul_album = request.POST.get('album')
        label = request.POST.get('label')
        judul_song = request.POST.get('judul')
        artist = request.POST.get('artist')
        songwriters = request.POST.getlist('songwriter')
        genres = request.POST.getlist('genre')
        durasi = request.POST.get('durasi')

        print(judul_album)
        print(label)
        print(judul_song)
        print(artist)
        print(songwriters)
        print(genres)
        print(durasi)

        # insert data ke ALBUM
        id_album = str(uuid.uuid4())
        cursor.execute(
            """INSERT INTO ALBUM(id, judul, jumlah_lagu, id_label, total_durasi) VALUES 
                (%s, %s, %s, %s, %s)""", 
                (id_album, judul_album, 1, label, durasi)
        )

        # insert data ke KONTEN
        id_konten = str(uuid.uuid4())
        tanggal_rilis = str(datetime.datetime.now())
        tahun = "2024"
        durasi = durasi
        cursor.execute(
            """INSERT INTO KONTEN(id, judul, tanggal_rilis, tahun, durasi) VALUES 
                (%s, %s, %s, %s, %s)""", 
                (id_konten, judul_song, tanggal_rilis, tahun, durasi)
        )

        # insert data ke SONG
        cursor.execute("SELECT ARTIST.id FROM ARTIST JOIN AKUN ON AKUN.email = ARTIST.email_akun WHERE AKUN.nama = %s", [artist])
        id_artist = cursor.fetchone()
        cursor.execute(
            """INSERT INTO SONG(id_konten, id_artist, id_album, total_play, total_download) VALUES 
                (%s, %s, %s, %s, %s)""", 
                (id_konten, id_artist, id_album, 0, 0)
        )

        # insert data ke royalti (songwriter)
        for songwriter in songwriters:
            print(str(songwriter))
            print("runnn")
            cursor.execute("SELECT id_pemilik_hak_cipta FROM SONGWRITER WHERE id = %s", [songwriter])
            id_songwriter  = cursor.fetchone()
            jumlah = random.randint(100, 999)
            cursor.execute(
                """INSERT INTO ROYALTI(id_pemilik_hak_cipta, id_song, jumlah) VALUES 
                    (%s, %s, %s)""", 
                    (id_songwriter[0], id_konten, jumlah)
            )

        # insert data ke royalti (artist)
        cursor.execute("SELECT ARTIST.id_pemilik_hak_cipta FROM AKUN JOIN ARTIST ON ARTIST.email_akun = AKUN.email WHERE AKUN.nama = %s ", [artist])
        id_artist = cursor.fetchone()
        jumlah = random.randint(100, 999)
        cursor.execute(
            """INSERT INTO ROYALTI(id_pemilik_hak_cipta, id_song, jumlah) VALUES 
                (%s, %s, %s)""", 
                (id_artist[0], id_konten, jumlah)
        )

        # insert data ke royalti (label)
        cursor.execute("SELECT LABEL.id_pemilik_hak_cipta FROM ALBUM JOIN LABEL ON ALBUM.id_label = LABEL.id WHERE ALBUM.id = %s ", [id_album])
        id_label = cursor.fetchone()
        jumlah = random.randint(100, 999)
        cursor.execute(
            """INSERT INTO ROYALTI(id_pemilik_hak_cipta, id_song, jumlah) VALUES 
                (%s, %s, %s)""", 
                (id_label[0], id_konten, jumlah)
        )

        # insert data ke songwriter_write_song
        for songwriter in songwriters:
            cursor.execute(
                """INSERT INTO SONGWRITER_WRITE_SONG(id_songwriter, id_song) VALUES 
                    (%s, %s)""", 
                    (songwriter, id_konten)
            )

        # insert data ke genre
        for genre in genres:
            cursor.execute(
                """INSERT INTO GENRE(id_konten, genre) VALUES 
                    (%s, %s)""", 
                    (id_konten, genre)
            )

        return HttpResponseRedirect(reverse('daftar_album_song:list_album'))
    
    cursor.execute("SELECT DISTINCT genre FROM GENRE")
    genre_list  = cursor.fetchall()
    
    cursor.execute("SELECT DISTINCT ARTIST.id, AKUN.nama FROM ARTIST, AKUN WHERE AKUN.email = ARTIST.email_akun")
    artist_list  = cursor.fetchall()

    cursor.execute("SELECT DISTINCT SONGWRITER.id, AKUN.nama FROM SONGWRITER, AKUN WHERE AKUN.email = SONGWRITER.email_akun")
    songwriter_list  = cursor.fetchall()

    cursor.execute("SELECT AKUN.nama FROM AKUN WHERE AKUN.email = %s ", [email])
    nama_akun  = cursor.fetchone()

    songwriter = ""

    if request.session.get('is_songwriter') :
        cursor.execute("SELECT SONGWRITER.id, AKUN.nama FROM AKUN JOIN SONGWRITER ON AKUN.email=SONGWRITER.email_akun WHERE AKUN.email = %s ", [email])
        songwriter  = cursor.fetchone()

    print(songwriter)

    cursor.execute("SELECT id, nama FROM LABEL;")
    label_list = cursor.fetchall()
    
    context = {
        "artist" : nama_akun[0],
        "songwriter_checked" : songwriter,
        "artist_list" : artist_list,
        "songwriter_list" : songwriter_list,
        "genre_list": genre_list,
        "label_list": label_list,
        'status_langganan': request.session.get('status_langganan'),
        'isArtist': request.session.get('is_artist'),
        'isSongwriter': request.session.get('is_songwriter'),
        'isPodcaster': request.session.get('is_podcaster'),
    }
    
    return render(request, 'create_album_songwriter_artist.html', context)


@connectdb
def list_song(cursor: CursorWrapper, request):
    id= request.GET.get("id")

    cursor.execute(rf"""SELECT judul 
                   FROM ALBUM 
                   WHERE ALBUM.id = '{id}';
                   """)
    album_judul = cursor.fetchone()

    query =(rf"""SELECT KONTEN.id, KONTEN.judul, SONG.total_play, SONG.total_download, KONTEN.durasi
                FROM KONTEN, SONG
                JOIN ALBUM ON SONG.id_album = ALBUM.id
                WHERE ALBUM.id = '{id}' AND KONTEN.id = SONG.id_konten;
                                """)
    cursor.execute(query)
    songs = cursor.fetchall()

    print(album_judul[0])
    
    context = {
        "album_id": id,
        "album_judul": album_judul[0],
        "songs": songs,
        'status_langganan': request.session.get('status_langganan'),
        'isArtist': request.session.get('is_artist'),
        'isSongwriter': request.session.get('is_songwriter'),
        'isPodcaster': request.session.get('is_podcaster'),
    }

    return render(request, 'list_song_songwriter_artist.html', context)

@connectdb
def create_song(cursor: CursorWrapper, request):
    id= request.GET.get("id")

    cursor.execute(rf"""SELECT judul 
                   FROM ALBUM 
                   WHERE ALBUM.id = '{id}';
                   """)
    album_judul = cursor.fetchone()

    try:
        email = request.session.get('email')
    except:
        return HttpResponseRedirect(reverse("authentication:login_user"))

    if request.method == 'POST':
        judul = request.POST.get('judul')
        artist = request.POST.get('artist')
        songwriters = request.POST.getlist('songwriter')
        genres = request.POST.getlist('genre')
        durasi = request.POST.get('durasi')

        print(judul)
        print(artist)
        print(songwriters)
        print(genres)
        print(durasi)

        # insert data ke KONTEN
        id_konten = str(uuid.uuid4())
        judul_song = judul
        tanggal_rilis = str(datetime.datetime.now())
        tahun = "2024"
        durasi = durasi
        cursor.execute(
            """INSERT INTO KONTEN(id, judul, tanggal_rilis, tahun, durasi) VALUES 
                (%s, %s, %s, %s, %s)""", 
                (id_konten, judul_song, tanggal_rilis, tahun, durasi)
        )

        # insert data ke SONG
        cursor.execute("SELECT ARTIST.id FROM ARTIST JOIN AKUN ON AKUN.email = ARTIST.email_akun WHERE AKUN.nama = %s", [artist])
        id_artist = cursor.fetchone()
        cursor.execute(
            """INSERT INTO SONG(id_konten, id_artist, id_album, total_play, total_download) VALUES 
                (%s, %s, %s, %s, %s)""", 
                (id_konten, id_artist, id, 0, 0)
        )

        # insert data ke royalti (songwriter)
        for songwriter in songwriters:
            print(str(songwriter))
            print("runnn")
            cursor.execute("SELECT id_pemilik_hak_cipta FROM SONGWRITER WHERE id = %s", [songwriter])
            id_songwriter  = cursor.fetchone()
            jumlah = random.randint(100, 999)
            cursor.execute(
                """INSERT INTO ROYALTI(id_pemilik_hak_cipta, id_song, jumlah) VALUES 
                    (%s, %s, %s)""", 
                    (id_songwriter[0], id_konten, jumlah)
            )

        # insert data ke royalti (artist)
        cursor.execute("SELECT ARTIST.id_pemilik_hak_cipta FROM AKUN JOIN ARTIST ON ARTIST.email_akun = AKUN.email WHERE AKUN.nama = %s ", [artist])
        id_artist = cursor.fetchone()
        jumlah = random.randint(100, 999)
        cursor.execute(
            """INSERT INTO ROYALTI(id_pemilik_hak_cipta, id_song, jumlah) VALUES 
                (%s, %s, %s)""", 
                (id_artist[0], id_konten, jumlah)
        )

        # insert data ke royalti (label)
        cursor.execute("SELECT LABEL.id_pemilik_hak_cipta FROM ALBUM JOIN LABEL ON ALBUM.id_label = LABEL.id WHERE ALBUM.id = %s ", [id])
        id_label = cursor.fetchone()
        jumlah = random.randint(100, 999)
        cursor.execute(
            """INSERT INTO ROYALTI(id_pemilik_hak_cipta, id_song, jumlah) VALUES 
                (%s, %s, %s)""", 
                (id_label[0], id_konten, jumlah)
        )

        # insert data ke songwriter_write_song
        for songwriter in songwriters:
            cursor.execute(
                """INSERT INTO SONGWRITER_WRITE_SONG(id_songwriter, id_song) VALUES 
                    (%s, %s)""", 
                    (songwriter, id_konten)
            )

        # insert data ke genre
        for genre in genres:
            cursor.execute(
                """INSERT INTO GENRE(id_konten, genre) VALUES 
                    (%s, %s)""", 
                    (id_konten, genre)
            )

        return HttpResponseRedirect(reverse('daftar_album_song:list_song')+ f'?id={id}')
    
    cursor.execute("SELECT DISTINCT genre FROM GENRE")
    genre_list  = cursor.fetchall()
    
    cursor.execute("SELECT DISTINCT ARTIST.id, AKUN.nama FROM ARTIST, AKUN WHERE AKUN.email = ARTIST.email_akun")
    artist_list  = cursor.fetchall()

    cursor.execute("SELECT DISTINCT SONGWRITER.id, AKUN.nama FROM SONGWRITER, AKUN WHERE AKUN.email = SONGWRITER.email_akun")
    songwriter_list  = cursor.fetchall()

    cursor.execute("SELECT AKUN.nama FROM AKUN WHERE AKUN.email = %s ", [email])
    nama_akun  = cursor.fetchone()

    songwriter = ""

    if request.session.get('is_songwriter') :
        cursor.execute("SELECT SONGWRITER.id, AKUN.nama FROM AKUN JOIN SONGWRITER ON AKUN.email=SONGWRITER.email_akun WHERE AKUN.email = %s ", [email])
        songwriter  = cursor.fetchone()

    print(songwriter)
    
    context = {
        "album_id": id,
        "artist" : nama_akun[0],
        "songwriter_checked" : songwriter,
        "album_judul": album_judul[0],
        "artist_list" : artist_list,
        "songwriter_list" : songwriter_list,
        "genre_list": genre_list,
        'status_langganan': request.session.get('status_langganan'),
        'isArtist': request.session.get('is_artist'),
        'isSongwriter': request.session.get('is_songwriter'),
        'isPodcaster': request.session.get('is_podcaster'),
    }
    
    return render(request, 'create_song_songwriter_artist.html', context)

@connectdb
def delete_song(cursor: CursorWrapper, request):
    id_song= request.GET.get("id_song")

    cursor.execute(rf"""SELECT id_album FROM SONG WHERE id_konten = '{id_song}';
                   """)
    id_album = cursor.fetchone()

    cursor.execute(rf"""DELETE FROM konten WHERE id = '{id_song}';
                   """)

    return HttpResponseRedirect(reverse('daftar_album_song:list_song')+ f'?id={id_album[0]}')

@connectdb
def delete_album(cursor: CursorWrapper, request):
    id= request.GET.get("id")

    cursor.execute(rf"""DELETE FROM album WHERE id = '{id}';
                   """)

    return HttpResponseRedirect(reverse('daftar_album_song:list_album'))

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