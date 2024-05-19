import psycopg2
from datetime import datetime
from django.contrib import messages
from django.shortcuts import render, redirect
from django.db.backends.utils import CursorWrapper
from utils.query import connectdb
from django.views.decorators.csrf import csrf_exempt

@connectdb
@csrf_exempt
def play_song(cursor: CursorWrapper, request, id_konten):
    if request.method == 'POST':
        progress = int(request.POST.get('songProgress', 0))
        if progress > 70:
            timestamp = datetime.now()
            email_pemain = request.session.get('email')

            cursor.execute("""
                INSERT INTO AKUN_PLAY_SONG (email_pemain, id_song, waktu)
                VALUES (%s, %s, %s)
            """, [email_pemain, str(id_konten), timestamp])

            cursor.execute("""
                UPDATE SONG
                SET total_play = total_play + 1
                WHERE id_konten = %s
            """, [str(id_konten)])

    cursor.execute("""
        SELECT k.judul, array_agg(DISTINCT g.genre) AS genres, ak.nama AS artist,
               array_agg(DISTINCT ak2.nama) AS songwriters, k.durasi, k.tanggal_rilis,
               k.tahun, s.total_play, s.total_download, a.judul AS album_judul
        FROM KONTEN k
        JOIN SONG s ON k.id = s.id_konten
        JOIN ARTIST ar ON s.id_artist = ar.id
        JOIN AKUN ak ON ar.email_akun = ak.email
        LEFT JOIN SONGWRITER_WRITE_SONG sws ON s.id_konten = sws.id_song
        LEFT JOIN SONGWRITER sw ON sws.id_songwriter = sw.id
        LEFT JOIN AKUN ak2 ON sw.email_akun = ak2.email
        LEFT JOIN GENRE g ON k.id = g.id_konten
        JOIN ALBUM a ON s.id_album = a.id
        WHERE k.id = %s
        GROUP BY k.judul, ak.nama, k.durasi, k.tanggal_rilis, k.tahun, s.total_play, s.total_download, a.judul;
    """, [str(id_konten)])
    song_data = cursor.fetchone()

    context = {
        'id_konten': id_konten,
        'song_title': song_data[0],
        'genres': song_data[1],
        'artist': song_data[2],
        'songwriters': song_data[3],
        'duration': song_data[4],
        'release_date': song_data[5],
        'year': song_data[6],
        'total_plays': song_data[7],
        'total_downloads': song_data[8],
        'album_title': song_data[9],
        'is_premium': request.session.get('is_premium')
    }

    return render(request, 'play_song.html', context)

@connectdb
@csrf_exempt
def add_song_to_user_playlist(cursor: CursorWrapper, request, id_konten):
    email = request.session.get('email')

    cursor.execute("""
        SELECT id_user_playlist, judul
        FROM USER_PLAYLIST
        WHERE email_pembuat = %s;
    """, [email])
    playlists = cursor.fetchall()

    cursor.execute("""
        SELECT k.judul, ak.nama AS artist
        FROM KONTEN k
        JOIN SONG s ON k.id = s.id_konten
        JOIN ARTIST ar ON s.id_artist = ar.id
        JOIN AKUN ak ON ar.email_akun = ak.email
        WHERE k.id = %s;
    """, [id_konten])
    song_data = cursor.fetchone()
    judul_lagu = song_data[0]
    nama_artis = song_data[1]

    if request.method == 'POST':
        id_user_playlist = request.POST.get('id_user_playlist')

        cursor.execute("""
            SELECT id_playlist, judul
            FROM USER_PLAYLIST
            WHERE id_user_playlist = %s
        """, [id_user_playlist])
        result = cursor.fetchone()

        if result is None:
            messages.error(request, "Playlist tidak ditemukan.")
            return redirect('play_song:play_song', id_konten=id_konten)
        id_playlist = result[0]
        judul_playlist = result[1]

        try:
            cursor.execute("""
                INSERT INTO PLAYLIST_SONG (id_playlist, id_song)
                VALUES (%s, %s)
            """, [id_playlist, id_konten])
            return render(request, 'berhasil_tambah_lagu.html', {
                'song_title': judul_lagu,
                'playlist_title': judul_playlist,
                'id_user_playlist': id_user_playlist,
                'id_konten': id_konten
            })
        
        except psycopg2.IntegrityError:
            return render(request, 'gagal_tambah_lagu.html', {
                'song_title': judul_lagu,
                'playlist_title': judul_playlist,
                'id_user_playlist': id_user_playlist,
                'id_konten': id_konten
            })

    return render(request, 'add_song_to_user_playlist.html', {
        'id_konten': id_konten,
        'playlists': playlists,
        'song_title': judul_lagu,
        'artist': nama_artis
    })

@connectdb
@csrf_exempt
def download_song(cursor: CursorWrapper, request, id_konten):
    email = request.session.get('email')
    if request.method == 'POST':
        id_user_playlist = request.POST.get('id_user_playlist')

        cursor.execute("SELECT judul FROM KONTEN WHERE id = %s", [id_konten])
        judul_lagu = cursor.fetchone()[0]

        try:
            cursor.execute("INSERT INTO DOWNLOADED_SONG (id_song, email_downloader) VALUES (%s, %s)", [id_konten, email])
            return render(request, 'berhasil_download_lagu.html', {
                'song_title': judul_lagu,
                'id_konten': id_konten,
                'id_user_playlist': id_user_playlist
            })
        
        except psycopg2.IntegrityError:
            return render(request, 'gagal_download_lagu.html', {
                'song_title': judul_lagu,
                'id_konten': id_konten,
                'id_user_playlist': id_user_playlist
            })