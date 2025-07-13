from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from utils.database import execute_query, execute_single_query
from utils.authentication import require_authentication

@api_view(['GET'])
@require_authentication
def get_royalty_info(request):
    """
    Feature 14: Get royalty information for artist or songwriter
    GET /api/royalty/
    """
    try:
        email = request.user_email
        if not email:
            return Response({'error': 'Not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)

        # Check if user is an artist
        artist = execute_single_query(
            "SELECT id, id_pemilik_hak_cipta FROM ARTIST WHERE email_akun = %s",
            [email]
        )
        
        # Check if user is a songwriter
        songwriter = execute_single_query(
            "SELECT id, id_pemilik_hak_cipta FROM SONGWRITER WHERE email_akun = %s",
            [email]
        )
        
        if not artist and not songwriter:
            return Response({'error': 'User is not an artist or songwriter'}, status=status.HTTP_403_FORBIDDEN)
        
        # Use a single query to get all royalties and avoid duplicates
        royalties = execute_query(
            """
            SELECT DISTINCT
                s.id_konten,
                k.judul AS song_judul, 
                a.judul AS album_judul, 
                s.total_play, 
                s.total_download, 
                phc.rate_royalti,
                (phc.rate_royalti * s.total_play) AS total_royalti
            FROM SONG s
            JOIN KONTEN k ON s.id_konten = k.id
            JOIN ALBUM a ON s.id_album = a.id
            JOIN PEMILIK_HAK_CIPTA phc ON (
                (s.id_artist = %s AND phc.id = %s) OR
                (s.id_konten IN (
                    SELECT sws.id_song 
                    FROM SONGWRITER_WRITE_SONG sws 
                    WHERE sws.id_songwriter = %s
                ) AND phc.id = %s)
            )
            WHERE (s.id_artist = %s OR s.id_konten IN (
                SELECT sws.id_song 
                FROM SONGWRITER_WRITE_SONG sws 
                WHERE sws.id_songwriter = %s
            ))
            ORDER BY total_royalti DESC, a.judul, k.judul
            """,
            [
                artist['id'] if artist else None,
                artist['id_pemilik_hak_cipta'] if artist else None,
                songwriter['id'] if songwriter else None,
                songwriter['id_pemilik_hak_cipta'] if songwriter else None,
                artist['id'] if artist else None,
                songwriter['id'] if songwriter else None
            ]
        )

        if not royalties:
            return Response({'error': 'User has no songs as artist or songwriter'}, status=status.HTTP_200_OK)

        # Calculate totals
        total_royalty = sum(item['total_royalti'] for item in royalties)
        total_plays = sum(item['total_play'] for item in royalties)
        total_downloads = sum(item['total_download'] for item in royalties)

        # Format response to match frontend expectations
        songs = []
        for item in royalties:
            songs.append({
                'id_konten': str(item['id_konten']),
                'judul': item['song_judul'],
                'album_judul': item['album_judul'],
                'total_play': item['total_play'],
                'total_download': item['total_download'],
                'royalty_play': item['total_royalti'],
                'royalty_download': 0,  # Download royalty can be calculated separately if needed
                'total_royalty': item['total_royalti'],
                'rate_royalti': item['rate_royalti']
            })

        return Response({
            'songs': songs,
            'total_royalty': total_royalty,
            'total_play': total_plays,
            'total_download': total_downloads,
            'summary': {
                'total_songs': len(royalties),
                'total_plays': total_plays,
                'total_downloads': total_downloads,
                'total_royalty': total_royalty,
                'total_royalty_formatted': f"Rp {total_royalty:,}".replace(',', '.')
            }
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@require_authentication
def get_label_royalty_info(request):
    """
    Feature 14: Get royalty information for label
    GET /api/royalty/label/
    """
    try:
        email = request.user_email
        if not email:
            return Response({'error': 'Not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Check if user is a label
        label = execute_single_query(
            "SELECT id, id_pemilik_hak_cipta FROM LABEL WHERE email = %s",
            [email]
        )
        
        if not label:
            return Response({'error': 'User is not a label'}, status=status.HTTP_403_FORBIDDEN)
        
        # Get label royalties from their albums
        royalty_data = execute_query(
            """
            SELECT 
                s.id_konten,
                k.judul AS song_judul, 
                a.judul AS album_judul, 
                s.total_play, 
                s.total_download, 
                phc.rate_royalti,
                (phc.rate_royalti * s.total_play) AS total_royalti
            FROM SONG s
            JOIN KONTEN k ON s.id_konten = k.id
            JOIN ALBUM a ON s.id_album = a.id
            JOIN LABEL l ON a.id_label = l.id
            JOIN PEMILIK_HAK_CIPTA phc ON l.id_pemilik_hak_cipta = phc.id
            WHERE l.email = %s
            ORDER BY total_royalti DESC, a.judul, k.judul
            """,
            [email]
        )
        
        # Calculate totals
        total_royalty = sum(item['total_royalti'] for item in royalty_data)
        total_plays = sum(item['total_play'] for item in royalty_data)
        total_downloads = sum(item['total_download'] for item in royalty_data)
        
        # Format response to match frontend expectations
        songs = []
        for item in royalty_data:
            songs.append({
                'id_konten': str(item['id_konten']),
                'judul': item['song_judul'],
                'album_judul': item['album_judul'],
                'total_play': item['total_play'],
                'total_download': item['total_download'],
                'royalty_play': item['total_royalti'],
                'royalty_download': 0,  # Download royalty can be calculated separately if needed
                'total_royalty': item['total_royalti'],
                'rate_royalti': item['rate_royalti']
            })
        
        return Response({
            'songs': songs,
            'total_royalty': total_royalty,
            'total_play': total_plays,
            'total_download': total_downloads,
            'summary': {
                'total_songs': len(royalty_data),
                'total_plays': total_plays,
                'total_downloads': total_downloads,
                'total_royalty': total_royalty,
                'total_royalty_formatted': f"Rp {total_royalty:,}".replace(',', '.')
            }
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@require_authentication
def update_royalty_info(request):
    """
    Update royalty information by recalculating based on current play counts
    POST /api/royalty/update/
    """
    try:
        email = request.user_email
        if not email:
            return Response({'error': 'Not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Update royalty for artists/songwriters
        updated_count = 0
        
        # Update artist royalties
        artist_updates = execute_query(
            """
            UPDATE ROYALTI 
            SET jumlah = phc.rate_royalti * s.total_play
            FROM PEMILIK_HAK_CIPTA phc, SONG s, ARTIST a
            WHERE ROYALTI.id_pemilik_hak_cipta = phc.id
            AND ROYALTI.id_song = s.id_konten
            AND phc.id = a.id_pemilik_hak_cipta
            AND a.email_akun = %s
            """,
            [email]
        )
        
        # Update songwriter royalties
        songwriter_updates = execute_query(
            """
            UPDATE ROYALTI 
            SET jumlah = phc.rate_royalti * s.total_play
            FROM PEMILIK_HAK_CIPTA phc, SONG s, SONGWRITER sw, SONGWRITER_WRITE_SONG sws
            WHERE ROYALTI.id_pemilik_hak_cipta = phc.id
            AND ROYALTI.id_song = s.id_konten
            AND phc.id = sw.id_pemilik_hak_cipta
            AND sw.id = sws.id_songwriter
            AND sws.id_song = s.id_konten
            AND sw.email_akun = %s
            """,
            [email]
        )
        
        # Update label royalties
        label_updates = execute_query(
            """
            UPDATE ROYALTI 
            SET jumlah = phc.rate_royalti * s.total_play
            FROM PEMILIK_HAK_CIPTA phc, SONG s, ALBUM a, LABEL l
            WHERE ROYALTI.id_pemilik_hak_cipta = phc.id
            AND ROYALTI.id_song = s.id_konten
            AND s.id_album = a.id
            AND a.id_label = l.id
            AND phc.id = l.id_pemilik_hak_cipta
            AND l.email = %s
            """,
            [email]
        )
        
        return Response({
            'message': 'Royalty information updated successfully',
            'updated_count': updated_count
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)