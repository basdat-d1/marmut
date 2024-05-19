from datetime import datetime
from django.shortcuts import render, redirect
from django.db.backends.utils import CursorWrapper
from django.http import JsonResponse
from utils.query import connectdb

@connectdb
def get_downloaded_songs(cursor: CursorWrapper, request):
    email = request.session.get('email')

    if email:
        cursor.execute("""
            SELECT KONTEN.id, KONTEN.judul, AKUN.nama AS artist
            FROM DOWNLOADED_SONG
            JOIN SONG ON DOWNLOADED_SONG.id_song = SONG.id_konten
            JOIN KONTEN ON SONG.id_konten = KONTEN.id
            JOIN ARTIST ON SONG.id_artist = ARTIST.id
            JOIN AKUN ON ARTIST.email_akun = AKUN.email
            WHERE DOWNLOADED_SONG.email_downloader = %s
        """, [email])
        downloaded_songs = cursor.fetchall()

        context = [
            {
                'id': str(song[0]),  # Pastikan ID adalah string
                'judul': song[1],
                'artist': song[2],
                'timestamp': datetime.now().strftime('%d/%m/%Y')
            }
            for song in downloaded_songs
        ]

        return JsonResponse({'downloaded_songs': context})
    else:
        return JsonResponse({'error': 'User not authenticated'}, status=401)

@connectdb
def delete_downloaded_song(cursor: CursorWrapper, request, song_id):
    email = request.session.get('email')

    if email and song_id:
        cursor.execute("""
            DELETE FROM DOWNLOADED_SONG
            WHERE email_downloader = %s AND id_song = %s
        """, [email, song_id])
        
        return redirect('downloaded_songs:downloaded_songs')
    else:
        return render(request, 'error.html', {'message': 'Invalid request'})

def downloaded_songs(request):
    return render(request, 'downloaded_songs.html')