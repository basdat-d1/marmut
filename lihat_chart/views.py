from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from utils.authentication import require_authentication
from utils.database import execute_query

@api_view(['GET'])
@require_authentication
def get_charts(request):
    try:
        # Return predefined chart types
        chart_types = [
            {'tipe': 'Daily Top 20'},
            {'tipe': 'Weekly Top 20'},
            {'tipe': 'Monthly Top 20'},
            {'tipe': 'Yearly Top 20'}
        ]
        
        return Response({
            'chart_types': [chart['tipe'] for chart in chart_types]
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@require_authentication
def get_chart_detail(request, chart_type):
    try:
        # Get chart items based on type
        if chart_type == 'Daily Top 20':
            chart_items = execute_query(
                """SELECT k.id, k.judul, ak.nama as artist_name,
                          k.tanggal_rilis, COALESCE(COUNT(aps.id_song), 0) as play_count
                   FROM SONG s
                   JOIN KONTEN k ON s.id_konten = k.id
                   JOIN ARTIST ar ON s.id_artist = ar.id
                   JOIN AKUN ak ON ar.email_akun = ak.email
                   LEFT JOIN AKUN_PLAY_SONG aps ON k.id = aps.id_song 
                        AND aps.waktu >= NOW() - INTERVAL '1 day'
                   GROUP BY k.id, k.judul, ak.nama, k.tanggal_rilis
                   ORDER BY play_count DESC
                   LIMIT 20""",
                []
            )
            
            return Response({
                'chart_type': chart_type,
                'items': [
                    {
                        'id': item['id'],
                        'judul': item['judul'],
                        'artist': item['artist_name'],
                        'tanggal_rilis': item['tanggal_rilis'].strftime('%d/%m/%Y') if item['tanggal_rilis'] else '',
                        'total_play': item['play_count']
                    } for item in chart_items
                ]
            }, status=status.HTTP_200_OK)
        elif chart_type == 'Weekly Top 20':
            chart_items = execute_query(
                """SELECT k.id, k.judul, ak.nama as artist_name,
                          k.tanggal_rilis, COALESCE(COUNT(aps.id_song), 0) as play_count
                   FROM SONG s
                   JOIN KONTEN k ON s.id_konten = k.id
                   JOIN ARTIST ar ON s.id_artist = ar.id
                   JOIN AKUN ak ON ar.email_akun = ak.email
                   LEFT JOIN AKUN_PLAY_SONG aps ON k.id = aps.id_song 
                        AND aps.waktu >= NOW() - INTERVAL '7 day'
                   GROUP BY k.id, k.judul, ak.nama, k.tanggal_rilis
                   ORDER BY play_count DESC
                   LIMIT 20""",
                []
            )
            return Response({
                'chart_type': chart_type,
                'items': [
                    {
                        'id': item['id'],
                        'judul': item['judul'],
                        'artist': item['artist_name'],
                        'tanggal_rilis': item['tanggal_rilis'].strftime('%d/%m/%Y') if item['tanggal_rilis'] else '',
                        'total_play': item['play_count']
                    } for item in chart_items
                ]
            }, status=status.HTTP_200_OK)
        elif chart_type == 'Monthly Top 20':
            chart_items = execute_query(
                """SELECT k.id, k.judul, ak.nama as artist_name,
                          k.tanggal_rilis, COALESCE(COUNT(aps.id_song), 0) as play_count
                   FROM SONG s
                   JOIN KONTEN k ON s.id_konten = k.id
                   JOIN ARTIST ar ON s.id_artist = ar.id
                   JOIN AKUN ak ON ar.email_akun = ak.email
                   LEFT JOIN AKUN_PLAY_SONG aps ON k.id = aps.id_song 
                        AND aps.waktu >= NOW() - INTERVAL '1 month'
                   GROUP BY k.id, k.judul, ak.nama, k.tanggal_rilis
                   ORDER BY play_count DESC
                   LIMIT 20""",
                []
            )
            return Response({
                'chart_type': chart_type,
                'items': [
                    {
                        'id': item['id'],
                        'judul': item['judul'],
                        'artist': item['artist_name'],
                        'tanggal_rilis': item['tanggal_rilis'].strftime('%d/%m/%Y') if item['tanggal_rilis'] else '',
                        'total_play': item['play_count']
                    } for item in chart_items
                ]
            }, status=status.HTTP_200_OK)
        elif chart_type == 'Yearly Top 20':
            chart_items = execute_query(
                """SELECT k.id, k.judul, ak.nama as artist_name,
                          k.tanggal_rilis, COALESCE(COUNT(aps.id_song), 0) as play_count
                   FROM SONG s
                   JOIN KONTEN k ON s.id_konten = k.id
                   JOIN ARTIST ar ON s.id_artist = ar.id
                   JOIN AKUN ak ON ar.email_akun = ak.email
                   LEFT JOIN AKUN_PLAY_SONG aps ON k.id = aps.id_song 
                        AND aps.waktu >= NOW() - INTERVAL '1 year'
                   GROUP BY k.id, k.judul, ak.nama, k.tanggal_rilis
                   ORDER BY play_count DESC
                   LIMIT 20""",
                []
            )
            return Response({
                'chart_type': chart_type,
                'items': [
                    {
                        'id': item['id'],
                        'judul': item['judul'],
                        'artist': item['artist_name'],
                        'tanggal_rilis': item['tanggal_rilis'].strftime('%d/%m/%Y') if item['tanggal_rilis'] else '',
                        'total_play': item['play_count']
                    } for item in chart_items
                ]
            }, status=status.HTTP_200_OK)
            
        else:
            return Response({'error': 'Invalid chart type'}, status=status.HTTP_400_BAD_REQUEST)
            
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@require_authentication
def get_trending_songs(request):
    """Get trending songs based on recent plays"""
    try:
        songs = execute_query(
            """SELECT k.id, k.judul, ak.nama as artist, a.judul as album,
                      s.total_play, s.total_download, k.tanggal_rilis
               FROM SONG s
               JOIN KONTEN k ON s.id_konten = k.id
               JOIN ARTIST ar ON s.id_artist = ar.id
               JOIN AKUN ak ON ar.email_akun = ak.email
               JOIN ALBUM a ON s.id_album = a.id
               WHERE k.tanggal_rilis >= CURRENT_DATE - INTERVAL '30 days'
               ORDER BY s.total_play DESC
               LIMIT 20""",
            []
        )
        
        return Response({
            'trending_songs': [
                {
                    'id': song['id'],
                    'judul': song['judul'],
                    'artist': song['artist'],
                    'album': song['album'],
                    'total_play': song['total_play'],
                    'total_download': song['total_download'],
                    'tanggal_rilis': song['tanggal_rilis'].strftime('%d/%m/%Y') if song['tanggal_rilis'] else ''
                } for song in songs
            ]
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@require_authentication
def get_top_downloads(request):
    """Get top downloaded songs"""
    try:
        songs = execute_query(
            """SELECT k.id, k.judul, ak.nama as artist, a.judul as album,
                      s.total_play, s.total_download, k.tanggal_rilis
               FROM SONG s
               JOIN KONTEN k ON s.id_konten = k.id
               JOIN ARTIST ar ON s.id_artist = ar.id
               JOIN AKUN ak ON ar.email_akun = ak.email
               JOIN ALBUM a ON s.id_album = a.id
               ORDER BY s.total_download DESC
               LIMIT 20""",
            []
        )
        
        return Response({
            'top_downloads': [
                {
                    'id': song['id'],
                    'judul': song['judul'],
                    'artist': song['artist'],
                    'album': song['album'],
                    'total_play': song['total_play'],
                    'total_download': song['total_download'],
                    'tanggal_rilis': song['tanggal_rilis'].strftime('%d/%m/%Y') if song['tanggal_rilis'] else ''
                } for song in songs
            ]
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)