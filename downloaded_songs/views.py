from django.shortcuts import render
from django.db.backends.utils import CursorWrapper
from django.http import JsonResponse
from utils.query import connectdb

@connectdb
def get_downloaded_songs(cursor: CursorWrapper, request):
    email = request.session.get('email', None)
    if email:
        cursor.execute("""
            SELECT KONTEN.judul, ARTIST.nama AS artist, DOWNLOADED_SONG.timestamp
            FROM DOWNLOADED_SONG
            JOIN SONG ON DOWNLOADED_SONG.id_song = SONG.id_konten
            JOIN KONTEN ON SONG.id_konten = KONTEN.id
            JOIN ARTIST ON SONG.id_artist = ARTIST.id
            WHERE DOWNLOADED_SONG.email_downloader = %s
        """, [email])
        downloaded_songs = cursor.fetchall()
        return JsonResponse({'downloaded_songs': downloaded_songs})
    else:
        return JsonResponse({'error': 'User not authenticated'}, status=401)

def downloaded_songs(request):
    return render(request, 'downloaded_songs.html')
