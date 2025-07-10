from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from utils.database import execute_query, execute_single_query, execute_delete_query
from utils.authentication import require_authentication

@api_view(['GET'])
@require_authentication
def get_downloaded_songs(request):
    """Get all downloaded songs for the authenticated user"""
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
            return Response({'error': 'Only premium users can access downloads'}, status=status.HTTP_403_FORBIDDEN)
        
        # Get downloaded songs
        songs = execute_query(
            """SELECT k.id, k.judul, ak.nama AS artist
               FROM DOWNLOADED_SONG ds
               JOIN SONG s ON ds.id_song = s.id_konten
               JOIN KONTEN k ON s.id_konten = k.id
               JOIN ARTIST ar ON s.id_artist = ar.id
               JOIN AKUN ak ON ar.email_akun = ak.email
               WHERE ds.email_downloader = %s""",
            [email]
        )
        
        return Response({
            'songs': [
                {
                    'id': song['id'],
                    'judul': song['judul'],
                    'artist': song['artist']
                } for song in songs
            ]
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
@require_authentication
def remove_downloaded_song(request, song_id):
    """Remove a song from downloads"""
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
            return Response({'error': 'Only premium users can manage downloads'}, status=status.HTTP_403_FORBIDDEN)
        
        # Get song info before deleting
        song_info = execute_single_query(
            """SELECT k.judul 
               FROM DOWNLOADED_SONG ds
               JOIN SONG s ON ds.id_song = s.id_konten
               JOIN KONTEN k ON s.id_konten = k.id
               WHERE ds.email_downloader = %s AND ds.id_song = %s""",
            [email, song_id]
        )
        
        if not song_info:
            return Response({'error': 'Song not found in downloads'}, status=status.HTTP_404_NOT_FOUND)
        
        # Remove from downloads
        execute_delete_query(
            "DELETE FROM DOWNLOADED_SONG WHERE email_downloader = %s AND id_song = %s",
            [email, song_id]
        )
        
        # Update song total_download count (decrease by 1)
        execute_query(
            "UPDATE SONG SET total_download = total_download - 1 WHERE id_konten = %s",
            [song_id], fetch=False
        )
        
        return Response({
            'message': f"Berhasil menghapus Lagu dengan judul '{song_info['judul']}' dari daftar unduhan!",
            'song_title': song_info['judul']
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@require_authentication
def get_download_stats(request):
    """Get download statistics for the authenticated user"""
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
            return Response({'error': 'Only premium users can access download stats'}, status=status.HTTP_403_FORBIDDEN)
        
        # Get download stats
        stats = execute_single_query(
            "SELECT COUNT(*) as total_downloads FROM DOWNLOADED_SONG WHERE email_downloader = %s",
            [email]
        )
        
        return Response({
            'stats': {
                'total_downloads': stats['total_downloads'] if stats else 0
            }
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)