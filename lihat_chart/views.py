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
                          k.tanggal_rilis, COUNT(aps.id_song) as play_count
                   FROM AKUN_PLAY_SONG aps
                   JOIN KONTEN k ON aps.id_song = k.id
                   JOIN SONG s ON k.id = s.id_konten
                   JOIN ARTIST ar ON s.id_artist = ar.id
                   JOIN AKUN ak ON ar.email_akun = ak.email
                   WHERE aps.waktu >= NOW() - INTERVAL '1 day'
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
                          k.tanggal_rilis, COUNT(aps.id_song) as play_count
                   FROM AKUN_PLAY_SONG aps
                   JOIN KONTEN k ON aps.id_song = k.id
                   JOIN SONG s ON k.id = s.id_konten
                   JOIN ARTIST ar ON s.id_artist = ar.id
                   JOIN AKUN ak ON ar.email_akun = ak.email
                   WHERE aps.waktu >= NOW() - INTERVAL '7 day'
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
                          k.tanggal_rilis, COUNT(aps.id_song) as play_count
                   FROM AKUN_PLAY_SONG aps
                   JOIN KONTEN k ON aps.id_song = k.id
                   JOIN SONG s ON k.id = s.id_konten
                   JOIN ARTIST ar ON s.id_artist = ar.id
                   JOIN AKUN ak ON ar.email_akun = ak.email
                   WHERE aps.waktu >= NOW() - INTERVAL '1 month'
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
                          k.tanggal_rilis, COUNT(aps.id_song) as play_count
                   FROM AKUN_PLAY_SONG aps
                   JOIN KONTEN k ON aps.id_song = k.id
                   JOIN SONG s ON k.id = s.id_konten
                   JOIN ARTIST ar ON s.id_artist = ar.id
                   JOIN AKUN ak ON ar.email_akun = ak.email
                   WHERE aps.waktu >= NOW() - INTERVAL '1 year'
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
            
        elif chart_type.lower() == 'artist':
            # Get top artists by total plays
            chart_items = execute_query(
                """SELECT ar.id, ak.nama as artist_name, 
                          COUNT(s.id_konten) as total_songs,
                          SUM(s.total_play) as total_plays
                   FROM ARTIST ar
                   JOIN AKUN ak ON ar.email_akun = ak.email
                   LEFT JOIN SONG s ON ar.id = s.id_artist
                   GROUP BY ar.id, ak.nama
                   ORDER BY total_plays DESC NULLS LAST
                   LIMIT 20""",
                []
            )
            
            return Response({
                'chart_type': chart_type,
                'items': [
                    {
                        'id': item['id'],
                        'type': 'artist',
                        'nama': item['artist_name'],
                        'total_songs': item['total_songs'],
                        'total_plays': item['total_plays'] or 0
                    } for item in chart_items
                ]
            }, status=status.HTTP_200_OK)
            
        elif chart_type.lower() == 'album':
            # Get top albums by total plays
            chart_items = execute_query(
                """SELECT a.id, a.judul as album_title, l.nama as label_name,
                          a.jumlah_lagu, a.total_durasi,
                          SUM(s.total_play) as total_plays
                   FROM ALBUM a
                   JOIN LABEL l ON a.id_label = l.id
                   LEFT JOIN SONG s ON a.id = s.id_album
                   GROUP BY a.id, a.judul, l.nama, a.jumlah_lagu, a.total_durasi
                   ORDER BY total_plays DESC NULLS LAST
                   LIMIT 20""",
                []
            )
            
            return Response({
                'chart_type': chart_type,
                'items': [
                    {
                        'id': item['id'],
                        'type': 'album',
                        'judul': item['album_title'],
                        'label': item['label_name'],
                        'jumlah_lagu': item['jumlah_lagu'],
                        'total_durasi': item['total_durasi'],
                        'total_plays': item['total_plays'] or 0
                    } for item in chart_items
                ]
            }, status=status.HTTP_200_OK)
            
        elif chart_type.lower() == 'playlist':
            # Get top playlists by play count
            chart_items = execute_query(
                """SELECT up.id_user_playlist, up.judul as playlist_title,
                          ak.nama as creator_name, up.jumlah_lagu, up.total_durasi,
                          COALESCE(SUM(aps.waktu), 0) as total_play_time
                   FROM USER_PLAYLIST up
                   JOIN AKUN ak ON up.email_pembuat = ak.email
                   LEFT JOIN AKUN_PLAY_USER_PLAYLIST aps ON up.id_user_playlist = aps.id_user_playlist
                   GROUP BY up.id_user_playlist, up.judul, ak.nama, up.jumlah_lagu, up.total_durasi
                   ORDER BY total_play_time DESC
                   LIMIT 20""",
                []
            )
            
            return Response({
                'chart_type': chart_type,
                'items': [
                    {
                        'id': item['id_user_playlist'],
                        'type': 'playlist',
                        'judul': item['playlist_title'],
                        'creator': item['creator_name'],
                        'jumlah_lagu': item['jumlah_lagu'],
                        'total_durasi': item['total_durasi'],
                        'total_play_time': item['total_play_time']
                    } for item in chart_items
                ]
            }, status=status.HTTP_200_OK)
            
        elif 'yearly' in chart_type.lower() or 'top 50' in chart_type.lower():
            # Get yearly top 50 songs
            chart_items = execute_query(
                """SELECT k.id, k.judul as song_title, ak.nama as artist_name,
                          a.judul as album_title, s.total_play, s.total_download
                   FROM SONG s
                   JOIN KONTEN k ON s.id_konten = k.id
                   JOIN ARTIST ar ON s.id_artist = ar.id
                   JOIN AKUN ak ON ar.email_akun = ak.email
                   JOIN ALBUM a ON s.id_album = a.id
                   WHERE k.tanggal_rilis >= CURRENT_DATE - INTERVAL '1 year'
                   ORDER BY s.total_play DESC
                   LIMIT 50""",
                []
            )
            
            return Response({
                'chart_type': chart_type,
                'items': [
                    {
                        'id': item['id'],
                        'type': 'song',
                        'judul': item['song_title'],
                        'artist': item['artist_name'],
                        'album': item['album_title'],
                        'total_play': item['total_play'],
                        'total_download': item['total_download']
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
                    'tanggal_rilis': song['tanggal_rilis']
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
                      s.total_play, s.total_download
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
                    'total_download': song['total_download']
                } for song in songs
            ]
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)