from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.db.backends.utils import CursorWrapper
from utils.query import connectdb

@connectdb
def get_downloaded_songs(cursor: CursorWrapper, request):
    email = request.session.get('email', None)
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
        print(downloaded_songs)  # Debugging: Print list of downloaded songs
        return downloaded_songs
    else:
        return []

@connectdb
def delete_downloaded_song(cursor: CursorWrapper, request, song_id):
    email = request.session.get('email', None)
    if email:
        cursor.execute("""
            DELETE FROM DOWNLOADED_SONG
            USING KONTEN, SONG
            WHERE DOWNLOADED_SONG.id_song = SONG.id_konten
            AND SONG.id_konten = KONTEN.id
            AND KONTEN.id = %s
            AND DOWNLOADED_SONG.email_downloader = %s
            RETURNING DOWNLOADED_SONG.id_song
        """, [song_id, email])
        deleted_song = cursor.fetchone()
        print(deleted_song)  # Debugging: Print ID of the deleted song
        if deleted_song:
            return True
    return False

def downloaded_songs(request):
    downloaded_songs = get_downloaded_songs(request)
    return render(request, 'downloaded_songs.html', {'downloaded_songs': downloaded_songs})

def delete_song(request, song_id):
    if request.method == 'POST':
        success = delete_downloaded_song(request, song_id)
        if success:
            return redirect('downloaded_songs:downloaded_songs')
    return JsonResponse({'success': False, 'message': 'Failed to delete song'})