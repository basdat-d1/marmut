from datetime import datetime
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from utils.authentication import require_authentication
from utils.database import execute_query, execute_single_query
from django.db import transaction
import uuid

@api_view(['GET'])
@require_authentication
def get_albums(request):
    """Get all albums"""
    try:
        albums = execute_query(
            """SELECT a.id, a.judul, l.nama as label, a.jumlah_lagu, a.total_durasi,
                      (SELECT k.tanggal_rilis 
                       FROM KONTEN k 
                       JOIN SONG s ON k.id = s.id_konten 
                       WHERE s.id_album = a.id 
                       ORDER BY k.tanggal_rilis ASC 
                       LIMIT 1) as tanggal_rilis
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
                    'total_durasi': album['total_durasi'],
                    'tanggal_rilis': album['tanggal_rilis'].strftime('%Y-%m-%d') if album['tanggal_rilis'] else None
                } for album in albums
            ]
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET', 'DELETE'])
@require_authentication
def get_album_detail(request, album_id):
    """Get album details with songs or delete album"""
    try:
        if request.method == 'DELETE':
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
            execute_query("DELETE FROM ALBUM WHERE id = %s", [album_id], fetch=False)
            
            return Response({
                'message': 'Album berhasil dihapus'
            }, status=status.HTTP_200_OK)
        
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
        
        # Get albums where user is involved with tanggal_rilis from first song
        albums = execute_query(
            """SELECT DISTINCT a.id, a.judul, l.nama as label, a.jumlah_lagu, a.total_durasi,
                      (SELECT k.tanggal_rilis 
                       FROM KONTEN k 
                       JOIN SONG s2 ON k.id = s2.id_konten 
                       WHERE s2.id_album = a.id 
                       ORDER BY k.tanggal_rilis ASC 
                       LIMIT 1) as tanggal_rilis
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
                    'total_durasi': album['total_durasi'],
                    'tanggal_rilis': album['tanggal_rilis'].strftime('%Y-%m-%d') if album['tanggal_rilis'] else None
                } for album in albums
            ]
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@require_authentication
def create_album(request):
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
        with transaction.atomic():
            execute_query(
                "INSERT INTO ALBUM (id, judul, id_label, jumlah_lagu, total_durasi) VALUES (%s, %s, %s, %s, %s)",
                [album_id, judul_album, label_id, 0, 0],
                fetch=False
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
        
        # Validate required fields
        if not all([album_id, judul_lagu, durasi]):
            return Response({'error': 'Semua field wajib diisi'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Convert durasi to integer if it's a string
        try:
            durasi = int(durasi)
        except (ValueError, TypeError):
            return Response({'error': 'Durasi harus berupa angka'}, status=status.HTTP_400_BAD_REQUEST)
        
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
        
        # If user is an artist and no artist_id provided, use current user's artist id
        if artist and not artist_id:
            artist_id = artist['id']
        
        # If user is songwriter and no artist_id provided, artist_id is required
        if songwriter and not artist and not artist_id:
            return Response({'error': 'Artist harus dipilih'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Validate artist_id exists if provided
        if artist_id:
            artist_exists = execute_single_query(
                "SELECT id FROM ARTIST WHERE id = %s",
                [artist_id]
            )
            if not artist_exists:
                return Response({'error': 'Artist tidak ditemukan'}, status=status.HTTP_404_NOT_FOUND)
        
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
        
        with transaction.atomic():
            # Insert into KONTEN
            execute_query(
                """INSERT INTO KONTEN (id, judul, tanggal_rilis, tahun, durasi) 
                   VALUES (%s, %s, %s, %s, %s)""",
                [song_id, judul_lagu, now.date(), now.year, durasi],
                fetch=False
            )
            
            # Insert into SONG
            execute_query(
                """INSERT INTO SONG (id_konten, id_artist, id_album, total_play, total_download) 
                   VALUES (%s, %s, %s, %s, %s)""",
                [song_id, artist_id, album_id, 0, 0],
                fetch=False
            )
            
            # Add genres
            for genre in genres:
                execute_query(
                    "INSERT INTO GENRE (id_konten, genre) VALUES (%s, %s)",
                    [song_id, genre],
                    fetch=False
                )
            
            # Add songwriters
            for songwriter_id in songwriter_ids:
                execute_query(
                    "INSERT INTO SONGWRITER_WRITE_SONG (id_songwriter, id_song) VALUES (%s, %s)",
                    [songwriter_id, song_id],
                    fetch=False
                )
            
            # Album stats are automatically updated by database trigger
        
        return Response({
            'message': 'Song berhasil dibuat',
            'song_id': song_id
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
@require_authentication
def delete_album(request, album_id):
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
        execute_query("DELETE FROM ALBUM WHERE id = %s", [album_id], fetch=False)
        
        return Response({
            'message': 'Album berhasil dihapus'
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
@require_authentication
def delete_song(request, song_id):
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
        
        # Delete song
        execute_query("DELETE FROM KONTEN WHERE id = %s", [song_id], fetch=False)
        
        return Response({
            'message': 'Song berhasil dihapus'
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@require_authentication
def get_label_albums(request):
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
            """
            SELECT a.id, a.judul, 
                   COUNT(s.id_konten) as jumlah_lagu,
                   COALESCE((SELECT SUM(k.durasi) FROM KONTEN k JOIN SONG s2 ON k.id = s2.id_konten WHERE s2.id_album = a.id), 0) as total_durasi,
                   (SELECT k2.tanggal_rilis 
                    FROM KONTEN k2 
                    JOIN SONG s2 ON k2.id = s2.id_konten 
                    WHERE s2.id_album = a.id 
                    ORDER BY k2.tanggal_rilis ASC 
                    LIMIT 1) as tanggal_rilis
            FROM ALBUM a
            LEFT JOIN SONG s ON a.id = s.id_album
            WHERE a.id_label = %s
            GROUP BY a.id, a.judul
            ORDER BY a.judul
            """,
            [label['id']]
        )
        
        return Response({
            'albums': [
                {
                    'id': album['id'],
                    'judul': album['judul'],
                    'jumlah_lagu': album['jumlah_lagu'],
                    'total_durasi': album['total_durasi'],
                    'tanggal_rilis': album['tanggal_rilis'].strftime('%Y-%m-%d') if album['tanggal_rilis'] else None
                } for album in albums
            ]
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@require_authentication
def get_label_album_songs(request, album_id):
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
        execute_query("DELETE FROM ALBUM WHERE id = %s", [album_id], fetch=False)
        
        return Response({
            'message': 'Album berhasil dihapus'
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
@require_authentication
def delete_label_song(request, song_id):
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

        # Delete song
        execute_query("DELETE FROM KONTEN WHERE id = %s", [song_id], fetch=False)
        
        return Response({
            'message': 'Song berhasil dihapus'
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@require_authentication
def get_user_songs(request):
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
            return Response({'error': 'Only artists and songwriters can view their songs'}, status=status.HTTP_403_FORBIDDEN)
        
        # Get songs where user is involved
        if artist:
            # User is an artist
            songs = execute_query(
                """SELECT k.id, k.judul, k.durasi, k.tanggal_rilis, s.total_play, s.total_download,
                          a.judul as album_judul, l.nama as label
                   FROM SONG s
                   JOIN KONTEN k ON s.id_konten = k.id
                   JOIN ALBUM a ON s.id_album = a.id
                   JOIN LABEL l ON a.id_label = l.id
                   WHERE s.id_artist = %s
                   ORDER BY k.tanggal_rilis DESC""",
                [artist['id']]
            )
        else:
            # User is a songwriter
            songs = execute_query(
                """SELECT k.id, k.judul, k.durasi, k.tanggal_rilis, s.total_play, s.total_download,
                          a.judul as album_judul, l.nama as label
                   FROM SONG s
                   JOIN KONTEN k ON s.id_konten = k.id
                   JOIN SONGWRITER_WRITE_SONG sws ON s.id_konten = sws.id_song
                   JOIN SONGWRITER sw ON sws.id_songwriter = sw.id
                   JOIN ALBUM a ON s.id_album = a.id
                   JOIN LABEL l ON a.id_label = l.id
                   WHERE sw.email_akun = %s
                   ORDER BY k.tanggal_rilis DESC""",
                [email]
            )
        
        return Response({
            'songs': [
                {
                    'id': song['id'],
                    'judul': song['judul'],
                    'durasi': song['durasi'],
                    'tanggal_rilis': song['tanggal_rilis'].isoformat() if song['tanggal_rilis'] else None,
                    'total_play': song['total_play'],
                    'total_download': song['total_download'],
                    'album': song['album_judul'],
                    'label': song['label']
                } for song in songs
            ]
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@require_authentication
def get_all_labels(request):
    """Get all labels"""
    try:
        labels = execute_query(
            "SELECT id, nama FROM LABEL ORDER BY nama",
            []
        )
        return Response({'labels': labels}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@require_authentication
def get_all_artists(request):
    """Get all artists"""
    try:
        artists = execute_query(
            "SELECT id, nama FROM ARTIST a JOIN AKUN ak ON a.email_akun = ak.email ORDER BY nama",
            []
        )
        return Response({'artists': artists}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@require_authentication
def get_all_songwriters(request):
    """Get all songwriters"""
    try:
        songwriters = execute_query(
            "SELECT id, nama FROM SONGWRITER s JOIN AKUN ak ON s.email_akun = ak.email ORDER BY nama",
            []
        )
        return Response({'songwriters': songwriters}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@require_authentication
def get_all_genres(request):
    """Get all unique genres"""
    try:
        genres = execute_query(
            "SELECT DISTINCT genre FROM GENRE ORDER BY genre",
            []
        )
        return Response({'genres': [g['genre'] for g in genres]}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)