import uuid
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import date
from django.http import HttpResponseRedirect
from django.db.backends.utils import CursorWrapper
from utils.query import connectdb

def convert_duration(total_minutes):
    hours = total_minutes // 60
    minutes = total_minutes % 60

    if hours >= 1:
        return f"{hours} jam {minutes} menit"
    else:
        return f"{minutes} menit"

@connectdb
def user_playlist(cursor: CursorWrapper, request):
    email_pembuat = request.session.get('email')

    cursor.execute("""
        SELECT id_user_playlist, judul, jumlah_lagu, total_durasi
        FROM USER_PLAYLIST
        WHERE email_pembuat = %s;
    """, [email_pembuat])
    playlists = cursor.fetchall()

    playlist_data = [{
        'id': playlist[0],
        'judul': playlist[1],
        'jumlah_lagu': playlist[2],
        'total_durasi': convert_duration(playlist[3])
    } for playlist in playlists]

    return render(request, "user_playlist.html", {'playlists': playlist_data})

@connectdb
def tambah_playlist(cursor: CursorWrapper, request):
    if request.method == 'POST':
        judul = request.POST.get('judul')
        deskripsi = request.POST.get('deskripsi')
        email_pembuat = request.session.get('email')

        id_user_playlist = str(uuid.uuid4())
        id_playlist = str(uuid.uuid4())
        tanggal_dibuat = date.today()

        cursor.execute("INSERT INTO PLAYLIST (id) VALUES (%s)", [id_playlist])
        cursor.execute("""
            INSERT INTO USER_PLAYLIST (email_pembuat, id_user_playlist, judul, deskripsi, jumlah_lagu, tanggal_dibuat, id_playlist, total_durasi)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, [email_pembuat, id_user_playlist, judul, deskripsi, 0, tanggal_dibuat, id_playlist, 0])

        return HttpResponseRedirect(reverse('user_playlist:user_playlist'))

    return render(request, 'tambah_playlist.html')

@connectdb
def ubah_playlist(cursor: CursorWrapper, request, id_user_playlist):
    if request.method == 'POST':
        judul = request.POST.get('judul')
        deskripsi = request.POST.get('deskripsi')

        cursor.execute("""
            UPDATE USER_PLAYLIST
            SET judul = %s, deskripsi = %s
            WHERE id_user_playlist = %s;
        """, [judul, deskripsi, id_user_playlist])
        messages.success(request, 'Playlist berhasil diubah.')
        return HttpResponseRedirect(reverse('user_playlist:user_playlist'))

    cursor.execute("""
        SELECT judul, deskripsi
        FROM USER_PLAYLIST
        WHERE id_user_playlist = %s;
    """, [id_user_playlist])
    playlist = cursor.fetchone()

    return render(request, 'ubah_playlist.html', {'playlist': {'id': id_user_playlist, 'judul': playlist[0], 'deskripsi': playlist[1]}})

@connectdb
def hapus_playlist(cursor: CursorWrapper, id_user_playlist):
    cursor.execute("""
        DELETE FROM USER_PLAYLIST
        WHERE id_user_playlist = %s;
    """, [id_user_playlist])

    return HttpResponseRedirect(reverse('user_playlist:user_playlist'))

@connectdb
def detail_playlist(cursor: CursorWrapper, request, id_user_playlist):
    cursor.execute("""
        SELECT UP.judul, UP.deskripsi, UP.jumlah_lagu, UP.total_durasi, UP.tanggal_dibuat, A.nama as pembuat
        FROM USER_PLAYLIST UP
        JOIN AKUN A ON UP.email_pembuat = A.email
        WHERE UP.id_user_playlist = %s;
    """, [id_user_playlist])
    playlist = cursor.fetchone()

    cursor.execute("""
        SELECT K.id, K.judul, AK.nama, K.durasi
        FROM PLAYLIST_SONG PS
        JOIN KONTEN K ON PS.id_song = K.id
        JOIN SONG S ON K.id = S.id_konten
        JOIN ARTIST AR ON S.id_artist = AR.id
        JOIN AKUN AK ON AR.email_akun = AK.email
        JOIN USER_PLAYLIST UP ON PS.id_playlist = UP.id_playlist
        WHERE UP.id_user_playlist = %s;
    """, [id_user_playlist])
    songs = cursor.fetchall()

    return render(request, 'detail_playlist.html', {
        'playlist': {
            'judul': playlist[0],
            'deskripsi': playlist[1],
            'jumlah_lagu': playlist[2],
            'total_durasi': convert_duration(playlist[3]),
            'tanggal_dibuat': playlist[4],
            'pembuat': playlist[5]
        },
        'songs': [{
            'id': song[0],
            'judul': song[1],
            'nama': song[2],
            'durasi': convert_duration(song[3])
        } for song in songs],
        'id_user_playlist': id_user_playlist
    })

@connectdb
def tambah_lagu_playlist(cursor: CursorWrapper, request, id_user_playlist):
    if request.method == 'POST':
        id_song = request.POST.get('id_song')

        cursor.execute("""
            SELECT id_playlist
            FROM USER_PLAYLIST
            WHERE id_user_playlist = %s
        """, [id_user_playlist])
        id_playlist = cursor.fetchone()[0]

        cursor.execute("""
            INSERT INTO PLAYLIST_SONG (id_playlist, id_song)
            VALUES (%s, %s)
        """, [id_playlist, id_song])

        return redirect('user_playlist:detail_playlist', id_user_playlist=id_user_playlist)

    cursor.execute("""
        SELECT K.id, K.judul, AK.nama AS nama_artis
        FROM KONTEN K
        JOIN SONG S ON K.id = S.id_konten
        JOIN ARTIST AR ON S.id_artist = AR.id
        JOIN AKUN AK ON AR.email_akun = AK.email
    """)
    songs = cursor.fetchall()

    song_choices = [(str(song[0]), f"{song[1]} - {song[2]}") for song in songs]
    return render(request, 'tambah_lagu.html', {
        'id_user_playlist': id_user_playlist,
        'song_choices': song_choices
    })

@connectdb
def hapus_lagu_playlist(cursor: CursorWrapper, request, id_user_playlist, id_song):
    cursor.execute("""
        DELETE FROM PLAYLIST_SONG
        WHERE id_playlist = (
            SELECT id_playlist
            FROM USER_PLAYLIST
            WHERE id_user_playlist = %s
        ) AND id_song = %s;
    """, [id_user_playlist, id_song])

    return HttpResponseRedirect(reverse('user_playlist:detail_playlist', args=[id_user_playlist]))