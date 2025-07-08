from datetime import datetime
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from utils.authentication import require_authentication
from utils.database import execute_query, execute_single_query, execute_insert_query, execute_update_query, execute_delete_query
import uuid

@api_view(['GET'])
@require_authentication
def get_albums(request):
    """Get all albums"""
    try:
        albums = execute_query(
            """SELECT a.id, a.judul, l.nama as label, a.jumlah_lagu, a.total_durasi
               FROM ALBUM a
               JOIN LABEL l ON a.id_label = l.id
               ORDER BY a.judul""",
            []
        )
        
        return Response({
            'albums': [
                {
                    'id': album['id'],
                    'judul': album['judul'],
                    'label': album['label'],
                    'jumlah_lagu': album['jumlah_lagu'],
                    'total_durasi': album['total_durasi']
                } for album in albums
            ]
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@require_authentication
def get_album_detail(request, album_id):
    """Get album details with songs"""
    try:
        # Get album info
        album = execute_single_query(
            """SELECT a.id, a.judul, l.nama as label, a.jumlah_lagu, a.total_durasi
               FROM ALBUM a
               JOIN LABEL l ON a.id_label = l.id
               WHERE a.id = %s""",
            [album_id]
        )
        
        if not album:
            return Response({'error': 'Album not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Get album songs
        songs = execute_query(
            """SELECT k.id, k.judul, ak.nama as artist, k.durasi, s.total_play, s.total_download
               FROM SONG s
               JOIN KONTEN k ON s.id_konten = k.id
               JOIN ARTIST ar ON s.id_artist = ar.id
               JOIN AKUN ak ON ar.email_akun = ak.email
               WHERE s.id_album = %s
               ORDER BY k.judul""",
            [album_id]
        )
        
        return Response({
            'album': {
                'id': album['id'],
                'judul': album['judul'],
                'label': album['label'],
                'jumlah_lagu': album['jumlah_lagu'],
                'total_durasi': album['total_durasi']
            },
            'songs': [
                {
                    'id': song['id'],
                    'judul': song['judul'],
                    'artist': song['artist'],
                    'durasi': song['durasi'],
                    'total_play': song['total_play'],
                    'total_download': song['total_download']
                } for song in songs
            ]
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@require_authentication
def get_songs(request):
    """Get all songs"""
    try:
        songs = execute_query(
            """SELECT k.id, k.judul, ak.nama as artist, a.judul as album, 
                      k.durasi, s.total_play, s.total_download
               FROM SONG s
               JOIN KONTEN k ON s.id_konten = k.id
               JOIN ARTIST ar ON s.id_artist = ar.id
               JOIN AKUN ak ON ar.email_akun = ak.email
               JOIN ALBUM a ON s.id_album = a.id
               ORDER BY k.judul""",
            []
        )
        
        return Response({
            'songs': [
                {
                    'id': song['id'],
                    'judul': song['judul'],
                    'artist': song['artist'],
                    'album': song['album'],
                    'durasi': song['durasi'],
                    'total_play': song['total_play'],
                    'total_download': song['total_download']
                } for song in songs
            ]
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@require_authentication
def get_popular_songs(request):
    """Get popular songs based on play count"""
    try:
        songs = execute_query(
            """SELECT k.id, k.judul, ak.nama as artist, a.judul as album, 
                      k.durasi, s.total_play, s.total_download
               FROM SONG s
               JOIN KONTEN k ON s.id_konten = k.id
               JOIN ARTIST ar ON s.id_artist = ar.id
               JOIN AKUN ak ON ar.email_akun = ak.email
               JOIN ALBUM a ON s.id_album = a.id
               ORDER BY s.total_play DESC
               LIMIT 50""",
            []
        )
        
        return Response({
            'songs': [
                {
                    'id': song['id'],
                    'judul': song['judul'],
                    'artist': song['artist'],
                    'album': song['album'],
                    'durasi': song['durasi'],
                    'total_play': song['total_play'],
                    'total_download': song['total_download']
                } for song in songs
            ]
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@require_authentication
def get_new_releases(request):
    """Get new song releases"""
    try:
        songs = execute_query(
            """SELECT k.id, k.judul, ak.nama as artist, a.judul as album, 
                      k.durasi, k.tanggal_rilis, s.total_play, s.total_download
               FROM SONG s
               JOIN KONTEN k ON s.id_konten = k.id
               JOIN ARTIST ar ON s.id_artist = ar.id
               JOIN AKUN ak ON ar.email_akun = ak.email
               JOIN ALBUM a ON s.id_album = a.id
               ORDER BY k.tanggal_rilis DESC
               LIMIT 50""",
            []
        )
        
        return Response({
            'songs': [
                {
                    'id': song['id'],
                    'judul': song['judul'],
                    'artist': song['artist'],
                    'album': song['album'],
                    'durasi': song['durasi'],
                    'tanggal_rilis': song['tanggal_rilis'],
                    'total_play': song['total_play'],
                    'total_download': song['total_download']
                } for song in songs
            ]
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@require_authentication
def get_user_albums(request):
    """
    Feature 13: Get albums owned by the authenticated artist/songwriter
    GET /api/album-song/user-albums/
    """
    try:
        email = request.user_email
        if not email:
            return Response({'error': 'Not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Check if user is artist or songwriter
        artist = execute_single_query(
            "SELECT id FROM ARTIST WHERE email_akun = %s",
            [email]
        )
        
        songwriter = execute_single_query(
            "SELECT id FROM SONGWRITER WHERE email_akun = %s",
            [email]
        )
        
        if not artist and not songwriter:
            return Response({'error': 'Only artists and songwriters can manage albums'}, status=status.HTTP_403_FORBIDDEN)
        
        # Get albums where user is involved
        albums = execute_query(
            """SELECT DISTINCT a.id, a.judul, l.nama as label, a.jumlah_lagu, a.total_durasi
               FROM ALBUM a
               JOIN LABEL l ON a.id_label = l.id
               JOIN SONG s ON a.id = s.id_album
               WHERE (s.id_artist IN (SELECT id FROM ARTIST WHERE email_akun = %s) OR
                      s.id_konten IN (SELECT id_song FROM SONGWRITER_WRITE_SONG WHERE id_songwriter IN (SELECT id FROM SONGWRITER WHERE email_akun = %s)))
               ORDER BY a.judul""",
            [email, email]
        )
        
        return Response({
            'albums': [
                {
                    'id': album['id'],
                    'judul': album['judul'],
                    'label': album['label'],
                    'jumlah_lagu': album['jumlah_lagu'],
                    'total_durasi': album['total_durasi']
                } for album in albums
            ]
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@require_authentication
def create_album(request):
    """
    Feature 13: Create a new album
    POST /api/album-song/create-album/
    """
    try:
        email = request.user_email
        if not email:
            return Response({'error': 'Not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
        
        data = request.data
        judul_album = data.get('judul_album')
        label_id = data.get('label_id')
        
        if not judul_album or not label_id:
            return Response({'error': 'Judul album dan label harus diisi'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if user is artist or songwriter
        artist = execute_single_query(
            "SELECT id FROM ARTIST WHERE email_akun = %s",
            [email]
        )
        
        songwriter = execute_single_query(
            "SELECT id FROM SONGWRITER WHERE email_akun = %s",
            [email]
        )
        
        if not artist and not songwriter:
            return Response({'error': 'Only artists and songwriters can create albums'}, status=status.HTTP_403_FORBIDDEN)
        
        # Check if label exists
        label = execute_single_query(
            "SELECT id FROM LABEL WHERE id = %s",
            [label_id]
        )
        
        if not label:
            return Response({'error': 'Label tidak ditemukan'}, status=status.HTTP_404_NOT_FOUND)
        
        # Create album
        album_id = str(uuid.uuid4())
        execute_query(
            "INSERT INTO ALBUM (id, judul, id_label, jumlah_lagu, total_durasi) VALUES (%s, %s, %s, %s, %s)",
            [album_id, judul_album, label_id, 0, 0]
        )
        
        return Response({
            'message': 'Album berhasil dibuat',
            'album_id': album_id
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@require_authentication
def create_song(request):
    """
    Feature 13: Create a new song
    POST /api/album-song/create-song/
    """
    try:
        email = request.user_email
        if not email:
            return Response({'error': 'Not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
        
        data = request.data
        album_id = data.get('album_id')
        judul_lagu = data.get('judul_lagu')
        artist_id = data.get('artist_id')
        songwriter_ids = data.get('songwriter_ids', [])
        genres = data.get('genres', [])
        durasi = data.get('durasi')
        
        if not all([album_id, judul_lagu, durasi]):
            return Response({'error': 'Semua field wajib diisi'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if user is artist or songwriter
        artist = execute_single_query(
            "SELECT id FROM ARTIST WHERE email_akun = %s",
            [email]
        )
        
        songwriter = execute_single_query(
            "SELECT id FROM SONGWRITER WHERE email_akun = %s",
            [email]
        )
        
        if not artist and not songwriter:
            return Response({'error': 'Only artists and songwriters can create songs'}, status=status.HTTP_403_FORBIDDEN)
        
        # Check if album exists
        album = execute_single_query(
            "SELECT id FROM ALBUM WHERE id = %s",
            [album_id]
        )
        
        if not album:
            return Response({'error': 'Album tidak ditemukan'}, status=status.HTTP_404_NOT_FOUND)
        
        # Create song
        song_id = str(uuid.uuid4())
        now = datetime.now()
        
        # Insert into KONTEN
        execute_query(
            """INSERT INTO KONTEN (id, judul, tanggal_rilis, tahun, durasi) 
               VALUES (%s, %s, %s, %s, %s)""",
            [song_id, judul_lagu, now.date(), now.year, durasi]
        )
        
        # Insert into SONG
        execute_query(
            """INSERT INTO SONG (id_konten, id_artist, id_album, total_play, total_download) 
               VALUES (%s, %s, %s, %s, %s)""",
            [song_id, artist_id, album_id, 0, 0]
        )
        
        # Add genres
        for genre in genres:
            execute_query(
                "INSERT INTO GENRE (id_konten, genre) VALUES (%s, %s)",
                [song_id, genre]
            )
        
        # Add songwriters
        for songwriter_id in songwriter_ids:
            execute_query(
                "INSERT INTO SONGWRITER_WRITE_SONG (id_songwriter, id_song) VALUES (%s, %s)",
                [songwriter_id, song_id]
            )
        
        # Update album stats
        execute_query(
            """UPDATE ALBUM 
               SET jumlah_lagu = jumlah_lagu + 1, 
                   total_durasi = total_durasi + %s 
               WHERE id = %s""",
            [durasi, album_id]
        )
        
        return Response({
            'message': 'Song berhasil dibuat',
            'song_id': song_id
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
@require_authentication
def delete_album(request, album_id):
    """
    Feature 13: Delete an album
    DELETE /api/album-song/album/{album_id}/
    """
    try:
        email = request.user_email
        if not email:
            return Response({'error': 'Not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Check if user is artist or songwriter
        artist = execute_single_query(
            "SELECT id FROM ARTIST WHERE email_akun = %s",
            [email]
        )
        
        songwriter = execute_single_query(
            "SELECT id FROM SONGWRITER WHERE email_akun = %s",
            [email]
        )
        
        if not artist and not songwriter:
            return Response({'error': 'Only artists and songwriters can delete albums'}, status=status.HTTP_403_FORBIDDEN)
        
        # Check if album exists and user has permission
        album = execute_single_query(
            """SELECT a.id FROM ALBUM a
               JOIN SONG s ON a.id = s.id_album
               WHERE a.id = %s AND (s.id_artist IN (SELECT id FROM ARTIST WHERE email_akun = %s) OR
                                   s.id_konten IN (SELECT id_song FROM SONGWRITER_WRITE_SONG WHERE id_songwriter IN (SELECT id FROM SONGWRITER WHERE email_akun = %s)))""",
            [album_id, email, email]
        )
        
        if not album:
            return Response({'error': 'Album tidak ditemukan atau tidak memiliki izin'}, status=status.HTTP_404_NOT_FOUND)
        
        # Delete album (cascade will handle related records)
        execute_query("DELETE FROM ALBUM WHERE id = %s", [album_id])
        
        return Response({
            'message': 'Album berhasil dihapus'
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
@require_authentication
def delete_song(request, song_id):
    """
    Feature 13: Delete a song
    DELETE /api/album-song/song/{song_id}/
    """
    try:
        email = request.user_email
        if not email:
            return Response({'error': 'Not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Check if user is artist or songwriter
        artist = execute_single_query(
            "SELECT id FROM ARTIST WHERE email_akun = %s",
            [email]
        )
        
        songwriter = execute_single_query(
            "SELECT id FROM SONGWRITER WHERE email_akun = %s",
            [email]
        )
        
        if not artist and not songwriter:
            return Response({'error': 'Only artists and songwriters can delete songs'}, status=status.HTTP_403_FORBIDDEN)
        
        # Check if song exists and user has permission
        song = execute_single_query(
            """SELECT s.id_konten, s.id_album, s.id_artist, k.durasi
               FROM SONG s
               JOIN KONTEN k ON s.id_konten = k.id
               WHERE s.id_konten = %s AND (s.id_artist IN (SELECT id FROM ARTIST WHERE email_akun = %s) OR
                                         s.id_konten IN (SELECT id_song FROM SONGWRITER_WRITE_SONG WHERE id_songwriter IN (SELECT id FROM SONGWRITER WHERE email_akun = %s)))""",
            [song_id, email, email]
        )
        
        if not song:
            return Response({'error': 'Song tidak ditemukan atau tidak memiliki izin'}, status=status.HTTP_404_NOT_FOUND)
        
        # Update album stats before deleting
        execute_query(
            """UPDATE ALBUM 
               SET jumlah_lagu = jumlah_lagu - 1, 
                   total_durasi = total_durasi - %s 
               WHERE id = %s""",
            [song['durasi'], song['id_album']]
        )
        
        # Delete song (cascade will handle related records)
        execute_query("DELETE FROM KONTEN WHERE id = %s", [song_id])
        
        return Response({
            'message': 'Song berhasil dihapus'
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@require_authentication
def get_label_albums(request):
    """
    Feature 16: Get albums owned by the authenticated label
    GET /api/album-song/label-albums/
    """
    try:
        email = request.user_email
        if not email:
            return Response({'error': 'Not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Check if user is a label
        label = execute_single_query(
            "SELECT id FROM LABEL WHERE email = %s",
            [email]
        )
        
        if not label:
            return Response({'error': 'Only labels can manage albums'}, status=status.HTTP_403_FORBIDDEN)
        
        # Get albums owned by the label
        albums = execute_query(
            """SELECT a.id, a.judul, a.jumlah_lagu, a.total_durasi
               FROM ALBUM a
               WHERE a.id_label = %s
               ORDER BY a.judul""",
            [label['id']]
        )
        
        return Response({
            'albums': [
                {
                    'id': album['id'],
                    'judul': album['judul'],
                    'jumlah_lagu': album['jumlah_lagu'],
                    'total_durasi': album['total_durasi']
                } for album in albums
            ]
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@require_authentication
def get_label_album_songs(request, album_id):
    """
    Feature 16: Get songs in a label's album
    GET /api/album-song/label-album/{album_id}/songs/
    """
    try:
        email = request.user_email
        if not email:
            return Response({'error': 'Not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Check if user is a label
        label = execute_single_query(
            "SELECT id FROM LABEL WHERE email = %s",
            [email]
        )
        
        if not label:
            return Response({'error': 'Only labels can view album songs'}, status=status.HTTP_403_FORBIDDEN)
        
        # Check if album belongs to the label
        album = execute_single_query(
            "SELECT id, judul FROM ALBUM WHERE id = %s AND id_label = %s",
            [album_id, label['id']]
        )
        
        if not album:
            return Response({'error': 'Album tidak ditemukan atau tidak memiliki izin'}, status=status.HTTP_404_NOT_FOUND)
        
        # Get album songs
        songs = execute_query(
            """SELECT k.id, k.judul, ak.nama as artist, k.durasi, s.total_play, s.total_download
               FROM SONG s
               JOIN KONTEN k ON s.id_konten = k.id
               JOIN ARTIST ar ON s.id_artist = ar.id
               JOIN AKUN ak ON ar.email_akun = ak.email
               WHERE s.id_album = %s
               ORDER BY k.judul""",
            [album_id]
        )
        
        return Response({
            'album': {
                'id': album['id'],
                'judul': album['judul']
            },
            'songs': [
                {
                    'id': song['id'],
                    'judul': song['judul'],
                    'artist': song['artist'],
                    'durasi': song['durasi'],
                    'total_play': song['total_play'],
                    'total_download': song['total_download']
                } for song in songs
            ]
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
@require_authentication
def delete_label_album(request, album_id):
    """
    Feature 16: Delete a label's album
    DELETE /api/album-song/label-album/{album_id}/
    """
    try:
        email = request.user_email
        if not email:
            return Response({'error': 'Not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Check if user is a label
        label = execute_single_query(
            "SELECT id FROM LABEL WHERE email = %s",
            [email]
        )
        
        if not label:
            return Response({'error': 'Only labels can delete albums'}, status=status.HTTP_403_FORBIDDEN)
        
        # Check if album belongs to the label
        album = execute_single_query(
            "SELECT id FROM ALBUM WHERE id = %s AND id_label = %s",
            [album_id, label['id']]
        )
        
        if not album:
            return Response({'error': 'Album tidak ditemukan atau tidak memiliki izin'}, status=status.HTTP_404_NOT_FOUND)
        
        # Delete album (cascade will handle related records)
        execute_query("DELETE FROM ALBUM WHERE id = %s", [album_id])
        
        return Response({
            'message': 'Album berhasil dihapus'
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
@require_authentication
def delete_label_song(request, song_id):
    """
    Feature 16: Delete a song from a label's album
    DELETE /api/album-song/label-song/{song_id}/
    """
    try:
        email = request.user_email
        if not email:
            return Response({'error': 'Not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Check if user is a label
        label = execute_single_query(
            "SELECT id FROM LABEL WHERE email = %s",
            [email]
        )
        
        if not label:
            return Response({'error': 'Only labels can delete songs'}, status=status.HTTP_403_FORBIDDEN)
        
        # Check if song belongs to a label's album
        song = execute_single_query(
            """SELECT s.id_konten, s.id_album, k.durasi
               FROM SONG s
               JOIN KONTEN k ON s.id_konten = k.id
               JOIN ALBUM a ON s.id_album = a.id
               WHERE s.id_konten = %s AND a.id_label = %s""",
            [song_id, label['id']]
        )
        
        if not song:
            return Response({'error': 'Song tidak ditemukan atau tidak memiliki izin'}, status=status.HTTP_404_NOT_FOUND)
        
        # Update album stats before deleting
        execute_query(
            """UPDATE ALBUM 
               SET jumlah_lagu = jumlah_lagu - 1, 
                   total_durasi = total_durasi - %s 
               WHERE id = %s""",
            [song['durasi'], song['id_album']]
        )
        
        # Delete song (cascade will handle related records)
        execute_query("DELETE FROM KONTEN WHERE id = %s", [song_id])
        
        return Response({
            'message': 'Song berhasil dihapus'
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)