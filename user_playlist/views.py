import uuid
from datetime import date
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from utils.database import execute_query, execute_single_query, execute_insert_query, execute_delete_query, execute_update_query
from utils.authentication import require_authentication

def convert_duration(total_minutes):
    hours = total_minutes // 60
    minutes = total_minutes % 60

    if hours >= 1:
        return f"{hours} jam {minutes} menit"
    else:
        return f"{minutes} menit"

@api_view(['GET'])
@require_authentication
def get_user_playlists(request):
    """Get all user playlists"""
    try:
        email = request.user_email
        
        playlists = execute_query(
            """SELECT id_user_playlist, judul, deskripsi, jumlah_lagu, total_durasi, tanggal_dibuat
        FROM USER_PLAYLIST
               WHERE email_pembuat = %s
               ORDER BY tanggal_dibuat DESC""",
            [email]
        )
        
        return Response({
            'playlists': [
                {
                    'id': playlist['id_user_playlist'],
                    'judul': playlist['judul'],
                    'deskripsi': playlist['deskripsi'],
                    'jumlah_lagu': playlist['jumlah_lagu'],
                    'total_durasi': convert_duration(playlist['total_durasi']),
                    'tanggal_dibuat': playlist['tanggal_dibuat']
                } for playlist in playlists
            ]
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@require_authentication
def create_playlist(request):
    """Create a new playlist"""
    try:
        email = request.user_email
        
        data = request.data
        judul = data.get('judul')
        deskripsi = data.get('deskripsi', '')
        
        if not judul:
            return Response({'error': 'Judul playlist harus diisi'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Generate UUIDs
        id_user_playlist = str(uuid.uuid4())
        id_playlist = str(uuid.uuid4())
        tanggal_dibuat = date.today()

        # Insert into PLAYLIST table first
        execute_query("INSERT INTO PLAYLIST (id) VALUES (%s)", [id_playlist])
        
        # Insert into USER_PLAYLIST table
        execute_query(
            """INSERT INTO USER_PLAYLIST (email_pembuat, id_user_playlist, judul, deskripsi, 
                                          jumlah_lagu, tanggal_dibuat, id_playlist, total_durasi)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
            [email, id_user_playlist, judul, deskripsi, 0, tanggal_dibuat, id_playlist, 0]
        )
        
        return Response({
            'message': 'Playlist berhasil dibuat',
            'playlist': {
                'id': id_user_playlist,
                'judul': judul,
                'deskripsi': deskripsi,
                'jumlah_lagu': 0,
                'total_durasi': '0 menit',
                'tanggal_dibuat': tanggal_dibuat
            }
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@require_authentication
def get_playlist_detail(request, playlist_id):
    """Get playlist details with songs"""
    try:
        email = request.user_email
        
        # Get playlist info
        playlist = execute_single_query(
            """SELECT up.id_user_playlist, up.judul, up.deskripsi, up.tanggal_dibuat, 
                      up.jumlah_lagu, up.total_durasi, up.email_pembuat, up.id_playlist
               FROM USER_PLAYLIST up
               WHERE up.id_user_playlist = %s""",
            [playlist_id]
        )
        
        if not playlist:
            return Response({'error': 'Playlist not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Get playlist songs
        songs = execute_query(
            """SELECT k.id, k.judul, ak.nama as artist, k.durasi, a.judul as album
               FROM PLAYLIST_SONG ps
               JOIN SONG s ON ps.id_song = s.id_konten
               JOIN KONTEN k ON s.id_konten = k.id
               JOIN ARTIST ar ON s.id_artist = ar.id
               JOIN AKUN ak ON ar.email_akun = ak.email
               JOIN ALBUM a ON s.id_album = a.id
               WHERE ps.id_playlist = %s
               ORDER BY k.judul""",
            [playlist['id_playlist']]
        )
        
        return Response({
            'playlist': {
                'id': playlist['id_user_playlist'],
                'judul': playlist['judul'],
                'deskripsi': playlist['deskripsi'],
                'jumlah_lagu': playlist['jumlah_lagu'],
                'total_durasi': convert_duration(playlist['total_durasi']),
                'tanggal_dibuat': playlist['tanggal_dibuat'],
                'email_pembuat': playlist['email_pembuat']
            },
            'songs': [
                {
                    'id': song['id'],
                    'judul': song['judul'],
                    'artist': song['artist'],
                    'album': song['album'],
                    'durasi': convert_duration(song['durasi'])
                } for song in songs
            ]
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PUT'])
@require_authentication
def update_playlist(request, playlist_id):
    """Update playlist details"""
    try:
        email = request.user_email
        
        # Check if playlist exists and belongs to user
        playlist = execute_single_query(
            "SELECT email_pembuat FROM USER_PLAYLIST WHERE id_user_playlist = %s",
            [playlist_id]
        )
        
        if not playlist:
            return Response({'error': 'Playlist not found'}, status=status.HTTP_404_NOT_FOUND)
        
        if playlist['email_pembuat'] != email:
            return Response({'error': 'Unauthorized to modify this playlist'}, status=status.HTTP_403_FORBIDDEN)
        
        data = request.data
        judul = data.get('judul')
        deskripsi = data.get('deskripsi', '')
        
        if not judul:
            return Response({'error': 'Judul playlist harus diisi'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Update playlist
        execute_update_query(
            """UPDATE USER_PLAYLIST 
            SET judul = %s, deskripsi = %s
               WHERE id_user_playlist = %s""",
            [judul, deskripsi, playlist_id]
        )
        
        return Response({
            'message': 'Playlist berhasil diperbarui',
            'playlist': {
                'id': playlist_id,
                'judul': judul,
                'deskripsi': deskripsi
            }
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
@require_authentication
def delete_playlist(request, playlist_id):
    """Delete a playlist"""
    try:
        email = request.user_email
        
        # Check if playlist exists and belongs to user
        playlist = execute_single_query(
            "SELECT email_pembuat FROM USER_PLAYLIST WHERE id_user_playlist = %s",
            [playlist_id]
        )
        
        if not playlist:
            return Response({'error': 'Playlist not found'}, status=status.HTTP_404_NOT_FOUND)
        
        if playlist['email_pembuat'] != email:
            return Response({'error': 'Unauthorized to delete this playlist'}, status=status.HTTP_403_FORBIDDEN)
        
        # Delete playlist (cascade will handle related records)
        execute_delete_query(
            "DELETE FROM USER_PLAYLIST WHERE id_user_playlist = %s",
            [playlist_id]
        )
        
        return Response({
            'message': 'Playlist berhasil dihapus'
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@require_authentication
def add_song_to_playlist(request, playlist_id):
    """Add a song to playlist"""
    try:
        email = request.user_email
        
        # Check if playlist exists and belongs to user
        playlist = execute_single_query(
            "SELECT email_pembuat, id_playlist FROM USER_PLAYLIST WHERE id_user_playlist = %s",
            [playlist_id]
        )
        
        if not playlist:
            return Response({'error': 'Playlist not found'}, status=status.HTTP_404_NOT_FOUND)
        
        if playlist['email_pembuat'] != email:
            return Response({'error': 'Unauthorized to modify this playlist'}, status=status.HTTP_403_FORBIDDEN)
        
        data = request.data
        song_id = data.get('song_id')
        
        if not song_id:
            return Response({'error': 'Song ID harus diisi'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if song exists
        song = execute_single_query(
            "SELECT id FROM KONTEN WHERE id = %s",
            [song_id]
        )
        
        if not song:
            return Response({'error': 'Song not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Check if song already in playlist
        existing = execute_single_query(
            "SELECT id_playlist FROM PLAYLIST_SONG WHERE id_playlist = %s AND id_song = %s",
            [playlist['id_playlist'], song_id]
        )
        
        if existing:
            return Response({'error': 'Song already in playlist'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Add song to playlist
        execute_query(
            "INSERT INTO PLAYLIST_SONG (id_playlist, id_song) VALUES (%s, %s)",
            [playlist['id_playlist'], song_id]
        )
        
        return Response({
            'message': 'Lagu berhasil ditambahkan ke playlist'
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
@require_authentication
def remove_song_from_playlist(request, playlist_id, song_id):
    """Remove a song from playlist"""
    try:
        email = request.user_email
        
        # Check if playlist exists and belongs to user
        playlist = execute_single_query(
            "SELECT email_pembuat, id_playlist FROM USER_PLAYLIST WHERE id_user_playlist = %s",
            [playlist_id]
        )
        
        if not playlist:
            return Response({'error': 'Playlist not found'}, status=status.HTTP_404_NOT_FOUND)
        
        if playlist['email_pembuat'] != email:
            return Response({'error': 'Unauthorized to modify this playlist'}, status=status.HTTP_403_FORBIDDEN)
        
        # Remove song from playlist
        execute_delete_query(
            "DELETE FROM PLAYLIST_SONG WHERE id_playlist = %s AND id_song = %s",
            [playlist['id_playlist'], song_id]
        )
        
        return Response({
            'message': 'Lagu berhasil dihapus dari playlist'
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)