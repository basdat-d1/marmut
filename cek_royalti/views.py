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
        
        royalties = []
        
        # Check if user is an artist
        artist = execute_single_query(
            "SELECT id FROM ARTIST WHERE email_akun = %s",
            [email]
        )
        
        if artist:
            artist_royalties = execute_query(
                """SELECT k.judul AS song_judul, a.judul AS album_judul, 
                          s.total_play, s.total_download, 
                          (phc.rate_royalti * s.total_play) AS total_royalti
                   FROM SONG s
                   JOIN ALBUM a ON s.id_album = a.id
                   JOIN ROYALTI r ON s.id_konten = r.id_song
                   JOIN PEMILIK_HAK_CIPTA phc ON r.id_pemilik_hak_cipta = phc.id
                   JOIN KONTEN k ON s.id_konten = k.id
                   WHERE phc.id IN (
                       SELECT id_pemilik_hak_cipta 
                       FROM ARTIST 
                       WHERE email_akun = %s
                   )
                   ORDER BY a.judul, k.judul""",
                [email]
            )
            royalties.extend(artist_royalties)
        
        # Check if user is a songwriter
        songwriter = execute_single_query(
            "SELECT id FROM SONGWRITER WHERE email_akun = %s",
            [email]
        )
        
        if songwriter:
            songwriter_royalties = execute_query(
                """SELECT k.judul AS song_judul, a.judul AS album_judul, 
                          s.total_play, s.total_download, 
                          (phc.rate_royalti * s.total_play) AS total_royalti
                   FROM SONG s
                   JOIN ALBUM a ON s.id_album = a.id
                   JOIN ROYALTI r ON s.id_konten = r.id_song
                   JOIN PEMILIK_HAK_CIPTA phc ON r.id_pemilik_hak_cipta = phc.id
                   JOIN KONTEN k ON s.id_konten = k.id
                   WHERE phc.id IN (
                       SELECT id_pemilik_hak_cipta 
                       FROM SONGWRITER 
                       WHERE email_akun = %s
                   )
                   ORDER BY a.judul, k.judul""",
                [email]
            )
            royalties.extend(songwriter_royalties)
        
        if not royalties and not artist and not songwriter:
            return Response({'error': 'User is not an artist or songwriter'}, status=status.HTTP_403_FORBIDDEN)
        
        # Calculate totals
        total_royalty = sum(royalty['total_royalti'] for royalty in royalties)
        total_plays = sum(royalty['total_play'] for royalty in royalties)
        total_downloads = sum(royalty['total_download'] for royalty in royalties)
        
        return Response({
            'royalties': [
                {
                    'song_judul': royalty['song_judul'],
                    'album_judul': royalty['album_judul'],
                    'total_play': royalty['total_play'],
                    'total_download': royalty['total_download'],
                    'total_royalti': royalty['total_royalti'],
                    'total_royalti_formatted': f"Rp {royalty['total_royalti']:,}".replace(',', '.')
                } for royalty in royalties
            ],
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
            "SELECT email FROM LABEL WHERE email = %s",
            [email]
        )
        
        if not label:
            return Response({'error': 'User is not a label'}, status=status.HTTP_403_FORBIDDEN)
        
        # Get label royalties
        royalties = execute_query(
            """SELECT k.judul AS song_judul, a.judul AS album_judul, 
                      s.total_play, s.total_download, 
                      (phc.rate_royalti * s.total_play) AS total_royalti
               FROM SONG s
               JOIN ALBUM a ON s.id_album = a.id
               JOIN ROYALTI r ON s.id_konten = r.id_song
               JOIN PEMILIK_HAK_CIPTA phc ON r.id_pemilik_hak_cipta = phc.id
               JOIN KONTEN k ON s.id_konten = k.id
               WHERE phc.id IN (
                   SELECT id_pemilik_hak_cipta 
                   FROM LABEL 
                   WHERE email = %s
               )
               ORDER BY a.judul, k.judul""",
            [email]
        )
        
        # Calculate totals
        total_royalty = sum(royalty['total_royalti'] for royalty in royalties)
        total_plays = sum(royalty['total_play'] for royalty in royalties)
        total_downloads = sum(royalty['total_download'] for royalty in royalties)
        
        return Response({
            'royalties': [
                {
                    'song_judul': royalty['song_judul'],
                    'album_judul': royalty['album_judul'],
                    'total_play': royalty['total_play'],
                    'total_download': royalty['total_download'],
                    'total_royalti': royalty['total_royalti'],
                    'total_royalti_formatted': f"Rp {royalty['total_royalti']:,}".replace(',', '.')
                } for royalty in royalties
            ],
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