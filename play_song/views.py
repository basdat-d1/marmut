from datetime import datetime
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from utils.authentication import require_authentication
from utils.database import execute_query, execute_single_query, execute_insert_query, execute_update_query

@api_view(['GET'])
@require_authentication
def get_song_detail(request, song_id):
    """Get detailed information about a song"""
    try:
        email = request.user_email
        if not email:
            return Response({'error': 'Not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Get song details
        song = execute_single_query(
            """SELECT k.id, k.judul, k.durasi, k.tanggal_rilis, k.tahun,
                      array_agg(DISTINCT g.genre) AS genres,
                      ak.nama AS artist,
                      s.total_play, s.total_download,
                      a.judul AS album_judul
               FROM KONTEN k
               JOIN SONG s ON k.id = s.id_konten
               JOIN ARTIST ar ON s.id_artist = ar.id
               JOIN AKUN ak ON ar.email_akun = ak.email
               LEFT JOIN GENRE g ON k.id = g.id_konten
               JOIN ALBUM a ON s.id_album = a.id
               WHERE k.id = %s
               GROUP BY k.id, k.judul, k.durasi, k.tanggal_rilis, k.tahun, ak.nama, s.total_play, s.total_download, a.judul""",
            [song_id]
        )
        
        if not song:
            return Response({'error': 'Song not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Get songwriters
        songwriters = execute_query(
            '''
            SELECT ak.nama
            FROM SONGWRITER_WRITE_SONG sws
            JOIN SONGWRITER sw ON sws.id_songwriter = sw.id
            JOIN AKUN ak ON sw.email_akun = ak.email
            WHERE sws.id_song = %s
            ''',
            [song_id]
        )
        
        # Check if user has downloaded this song
        downloaded = execute_single_query(
            "SELECT id_song FROM DOWNLOADED_SONG WHERE email_downloader = %s AND id_song = %s",
            [email, song_id]
        )
        
        # Check if user is premium
        is_premium = execute_single_query(
            "SELECT email FROM PREMIUM WHERE email = %s",
            [email]
        )
        
        return Response({
            'song': {
                'id': song['id'],
                'judul': song['judul'],
                'artist': song['artist'],
                'album': song['album_judul'],
                'durasi': song['durasi'],
                'tanggal_rilis': song['tanggal_rilis'],
                'tahun': song['tahun'],
                'genres': song['genres'] or [],
                'songwriters': [sw['nama'] for sw in songwriters],
                'total_play': song['total_play'],
                'total_download': song['total_download'],
                'is_downloaded': bool(downloaded),
                'is_premium': bool(is_premium)
            }
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@require_authentication
def play_song(request, song_id):
    """
    Feature 8: Record a song play with progress tracking
    POST /api/play-song/{song_id}/
    """
    try:
        email = request.user_email
        if not email:
            return Response({'error': 'Not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
        
        data = request.data
        progress = data.get('progress', 0)
        
        # Validate progress value (0-100)
        if not isinstance(progress, (int, float)) or progress < 0 or progress > 100:
            return Response({
                'error': 'Progress harus berupa angka antara 0-100'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if song exists
        song = execute_single_query(
            "SELECT * FROM SONG WHERE id_konten = %s",
            [song_id]
        )
        
        if not song:
            return Response({'error': 'Song not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Only record play if progress > 70%
        if progress > 70:
            now = datetime.now()
            execute_query(
                """INSERT INTO AKUN_PLAY_SONG (email_pemain, id_song, waktu)
                   VALUES (%s, %s, %s)""",
                [email, song_id, now], fetch=False
            )
            
            # Update total play count
            execute_query(
                "UPDATE SONG SET total_play = total_play + 1 WHERE id_konten = %s",
                [song_id], fetch=False
            )
            
            return Response({
                'message': 'Song play recorded successfully',
                'progress': progress,
                'play_counted': True
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'message': 'Progress tidak cukup untuk mencatat play',
                'progress': progress,
                'play_counted': False
            }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@require_authentication
def download_song(request, song_id):
    """Download a song (premium only)"""
    try:
        email = request.user_email
        if not email:
            return Response({'error': 'Not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Check if user is premium
        premium_check = execute_single_query(
            "SELECT email FROM PREMIUM WHERE email = %s",
            [email]
        )
        
        if not premium_check:
            return Response({'error': 'Premium subscription required'}, status=status.HTTP_403_FORBIDDEN)
        
        # Check if song exists
        song = execute_single_query(
            "SELECT * FROM SONG WHERE id_konten = %s",
            [song_id]
        )
        
        if not song:
            return Response({'error': 'Song not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Check if already downloaded
        existing_download = execute_single_query(
            "SELECT * FROM DOWNLOADED_SONG WHERE email_downloader = %s AND id_song = %s",
            [email, song_id]
        )
        
        if existing_download:
            return Response({'message': 'Song already downloaded', 'warning': True}, status=status.HTTP_200_OK)
        
        # Add to downloads
        execute_insert_query(
            "INSERT INTO DOWNLOADED_SONG (email_downloader, id_song) VALUES (%s, %s)",
            [email, song_id]
        )
        
        # Update download count (handled by trigger)
        # execute_update_query(
        #     "UPDATE SONG SET total_download = total_download + 1 WHERE id_konten = %s",
        #     [song_id]
        # )
        
        return Response({'message': 'Song downloaded successfully', 'success': True}, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@require_authentication
def add_to_playlist(request, song_id):
    """Add a song to a user playlist"""
    try:
        email = request.user_email
        if not email:
            return Response({'error': 'Not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
        
        data = request.data
        playlist_id = data.get('playlist_id')
        
        if not playlist_id:
            return Response({'error': 'Playlist ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if song exists
        song = execute_single_query(
            "SELECT * FROM SONG WHERE id_konten = %s",
            [song_id]
        )
        
        if not song:
            return Response({'error': 'Song not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Check if playlist exists and belongs to user
        playlist = execute_single_query(
            "SELECT * FROM USER_PLAYLIST WHERE id_user_playlist = %s AND email_pembuat = %s",
            [playlist_id, email]
        )
        
        if not playlist:
            return Response({'error': 'Playlist not found or not owned by user'}, status=status.HTTP_404_NOT_FOUND)
        
        # Check if song is already in playlist
        existing = execute_single_query(
            "SELECT * FROM PLAYLIST_SONG WHERE id_playlist = %s AND id_song = %s",
            [playlist_id, song_id]
        )
        
        if existing:
            return Response({'message': 'Song already in playlist', 'warning': True}, status=status.HTTP_200_OK)
        
        # Add song to playlist
        execute_insert_query(
            "INSERT INTO PLAYLIST_SONG (id_playlist, id_song) VALUES (%s, %s)",
            [playlist_id, song_id]
        )
        
        return Response({'message': 'Song added to playlist successfully'}, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@require_authentication
def get_user_playlists_for_song(request):
    """Get user playlists for adding songs"""
    try:
        email = request.user_email
        if not email:
            return Response({'error': 'Not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
        
        playlists = execute_query(
            """SELECT up.id_user_playlist, up.judul, up.deskripsi, up.jumlah_lagu
               FROM USER_PLAYLIST up
               WHERE up.email_pembuat = %s
               ORDER BY up.tanggal_dibuat DESC""",
            [email]
        )
        
        return Response({
            'playlists': [
                {
                    'id': playlist['id_user_playlist'],
                    'judul': playlist['judul'],
                    'deskripsi': playlist['deskripsi'],
                    'jumlah_lagu': playlist['jumlah_lagu']
                } for playlist in playlists
            ]
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)