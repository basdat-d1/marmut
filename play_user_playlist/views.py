from datetime import datetime
from django.shortcuts import render, redirect
from django.db.backends.utils import CursorWrapper
from django.views.decorators.csrf import csrf_exempt
from utils.query import connectdb

def convert_duration(total_minutes):
    hours = total_minutes // 60
    minutes = total_minutes % 60

    if hours >= 1:
        return f"{hours} jam {minutes} menit"
    else:
        return f"{minutes} menit"

@connectdb
@csrf_exempt
def play_user_playlist(cursor: CursorWrapper, request, id_user_playlist):
    email = request.session.get('email')

    cursor.execute("""
        SELECT UP.judul, UP.deskripsi, UP.jumlah_lagu, UP.total_durasi, UP.tanggal_dibuat, A.nama as pembuat, UP.email_pembuat
        FROM USER_PLAYLIST UP
        JOIN AKUN A ON UP.email_pembuat = A.email
        WHERE UP.id_user_playlist = %s;
    """, [id_user_playlist])
    playlist = cursor.fetchone()

    cursor.execute("""
        SELECT K.id, K.judul, AK.nama AS nama_artis, K.durasi
        FROM PLAYLIST_SONG PS
        JOIN KONTEN K ON PS.id_song = K.id
        JOIN SONG S ON K.id = S.id_konten
        JOIN ARTIST AR ON S.id_artist = AR.id
        JOIN AKUN AK ON AR.email_akun = AK.email
        JOIN USER_PLAYLIST UP ON PS.id_playlist = UP.id_playlist
        WHERE UP.id_user_playlist = %s;
    """, [id_user_playlist])
    songs = cursor.fetchall()

    if request.method == 'POST':
        timestamp = datetime.now()
        cursor.execute("""
            INSERT INTO AKUN_PLAY_USER_PLAYLIST (email_pemain, id_user_playlist, email_pembuat, waktu)
            VALUES (%s, %s, %s, %s)
        """, [email, id_user_playlist, playlist['email_pembuat'], timestamp])

        for song in songs:
            cursor.execute("""
                INSERT INTO AKUN_PLAY_SONG (email_pemain, id_song, waktu)
                VALUES (%s, %s, %s)
            """, [email, song[0], timestamp])

        return redirect('play_user_playlist:play_user_playlist', id_user_playlist=id_user_playlist)

    return render(request, 'play_user_playlist.html', {
        'playlist': {
            'judul': playlist[0],
            'deskripsi': playlist[1],
            'jumlah_lagu': playlist[2],
            'total_durasi': convert_duration(playlist[3]),
            'tanggal_dibuat': playlist[4],
            'pembuat': playlist[5],
            'email_pembuat': playlist[6]
        },
        'songs': [{'id': song[0], 'judul': song[1], 'nama_artis': song[2], 'durasi': convert_duration(song[3])} for song in songs],
        'id_user_playlist': id_user_playlist
    })