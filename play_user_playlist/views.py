from datetime import datetime
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from utils.authentication import require_authentication
from utils.database import execute_query, execute_single_query, execute_insert_query

def convert_duration(total_minutes):
    hours = total_minutes // 60
    minutes = total_minutes % 60

    if hours >= 1:
        return f"{hours} jam {minutes} menit"
    else:
        return f"{minutes} menit"

@api_view(['GET', 'POST'])
@require_authentication
def play_user_playlist(request, id_user_playlist):
    """
    Feature 11: Get playlist details and handle playlist play
    GET /api/play-user-playlist/{id_user_playlist}/
    POST /api/play-user-playlist/{id_user_playlist}/
    """
    try:
        email = request.user_email
        if not email:
            return Response({'error': 'Not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Get playlist details
        playlist = execute_single_query(
            """SELECT up.judul, up.deskripsi, up.jumlah_lagu, up.total_durasi, 
                      up.tanggal_dibuat, ak.nama as pembuat, up.email_pembuat
               FROM USER_PLAYLIST up
               JOIN AKUN ak ON up.email_pembuat = ak.email
               WHERE up.id_user_playlist = %s""",
            [id_user_playlist]
        )
        
        if not playlist:
            return Response({'error': 'Playlist not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Get playlist songs
        songs = execute_query(
            """SELECT k.id, k.judul, ak.nama AS nama_artis, k.durasi
               FROM PLAYLIST_SONG ps
               JOIN KONTEN k ON ps.id_song = k.id
               JOIN SONG s ON k.id = s.id_konten
               JOIN ARTIST ar ON s.id_artist = ar.id
               JOIN AKUN ak ON ar.email_akun = ak.email
               JOIN USER_PLAYLIST up ON ps.id_playlist = up.id_playlist
               WHERE up.id_user_playlist = %s
               ORDER BY k.judul""",
            [id_user_playlist]
        )
        
        # Handle POST request (play playlist)
        if request.method == 'POST':
            timestamp = datetime.now()
            
            # Record playlist play
            execute_insert_query(
                """INSERT INTO AKUN_PLAY_USER_PLAYLIST (email_pemain, id_user_playlist, email_pembuat, waktu)
                   VALUES (%s, %s, %s, %s)""",
                [email, id_user_playlist, playlist['email_pembuat'], timestamp]
            )
            
            # Record individual song plays
            for song in songs:
                execute_insert_query(
                    """INSERT INTO AKUN_PLAY_SONG (email_pemain, id_song, waktu)
                       VALUES (%s, %s, %s)""",
                    [email, song['id'], timestamp]
                )
            
            return Response({
                'message': 'Playlist played successfully',
                'timestamp': timestamp
            }, status=status.HTTP_200_OK)
        
        # Handle GET request (get playlist details)
        return Response({
            'playlist': {
                'judul': playlist['judul'],
                'deskripsi': playlist['deskripsi'],
                'jumlah_lagu': playlist['jumlah_lagu'],
                'total_durasi': convert_duration(playlist['total_durasi']),
                'tanggal_dibuat': playlist['tanggal_dibuat'],
                'pembuat': playlist['pembuat'],
                'email_pembuat': playlist['email_pembuat']
            },
            'songs': [
                {
                    'id': song['id'],
                    'judul': song['judul'],
                    'nama_artis': song['nama_artis'],
                    'durasi': convert_duration(song['durasi'])
                } for song in songs
            ]
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@require_authentication
def play_song_from_playlist(request, id_user_playlist, song_id):
    """
    Feature 11: Play individual song from playlist
    POST /api/play-user-playlist/{id_user_playlist}/song/{song_id}/
    """
    try:
        email = request.user_email
        if not email:
            return Response({'error': 'Not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Check if song exists in playlist
        song_in_playlist = execute_single_query(
            """SELECT k.id, k.judul, ak.nama AS nama_artis, k.durasi
               FROM PLAYLIST_SONG ps
               JOIN KONTEN k ON ps.id_song = k.id
               JOIN SONG s ON k.id = s.id_konten
               JOIN ARTIST ar ON s.id_artist = ar.id
               JOIN AKUN ak ON ar.email_akun = ak.email
               JOIN USER_PLAYLIST up ON ps.id_playlist = up.id_playlist
               WHERE up.id_user_playlist = %s AND k.id = %s""",
            [id_user_playlist, song_id]
        )
        
        if not song_in_playlist:
            return Response({'error': 'Song not found in playlist'}, status=status.HTTP_404_NOT_FOUND)
        
        # Record individual song play
        timestamp = datetime.now()
        execute_query(
            """INSERT INTO AKUN_PLAY_SONG (email_pemain, id_song, waktu)
               VALUES (%s, %s, %s)""",
            [email, song_id, timestamp]
        )
        
        # Update song play count
        execute_query(
            "UPDATE SONG SET total_play = total_play + 1 WHERE id_konten = %s",
            [song_id]
        )
        
        return Response({
            'message': 'Song played successfully',
            'song': {
                'id': song_in_playlist['id'],
                'judul': song_in_playlist['judul'],
                'nama_artis': song_in_playlist['nama_artis'],
                'durasi': convert_duration(song_in_playlist['durasi'])
            },
            'timestamp': timestamp
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)