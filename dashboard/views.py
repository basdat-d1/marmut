from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from utils.database import fetch_one, fetch_all
from utils.authentication import require_authentication

@api_view(['GET'])
@require_authentication
def dashboard(request):
    """
    Feature 4: Dashboard for all user types
    GET /api/dashboard/
    """
    try:
        user_email = request.user_email
        user_type = request.user_type
        
        if user_type == 'label':
            return get_label_dashboard(user_email)
        else:
            return get_user_dashboard(user_email, request.user_roles)
            
    except Exception as e:
        return Response({
            'error': f'Terjadi kesalahan: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def get_user_dashboard(user_email, user_roles):
    """Get dashboard for regular users"""
    try:
        # Get basic user info
        user_query = """
            SELECT email, nama, is_verified, kota_asal, gender, 
                   tempat_lahir, tanggal_lahir
            FROM AKUN 
            WHERE email = %s
        """
        user = fetch_one(user_query, [user_email])
        
        if not user:
            return Response({
                'error': 'User tidak ditemukan'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Check premium status
        premium_query = "SELECT email FROM PREMIUM WHERE email = %s"
        is_premium = bool(fetch_one(premium_query, [user_email]))
        
        # Get subscription info if premium
        subscription_info = None
        if is_premium:
            subscription_query = """
                SELECT jenis_paket, timestamp_dimulai, timestamp_berakhir, metode_bayar
                FROM TRANSACTION 
                WHERE email = %s AND timestamp_berakhir > NOW()
                ORDER BY timestamp_berakhir DESC
                LIMIT 1
            """
            subscription = fetch_one(subscription_query, [user_email])
            if subscription:
                subscription_info = {
                    'jenis': subscription['jenis_paket'],
                    'mulai': subscription['timestamp_dimulai'].isoformat(),
                    'berakhir': subscription['timestamp_berakhir'].isoformat(),
                    'metode_bayar': subscription['metode_bayar']
                }
        
        # Create response that matches frontend expectations
        dashboard_data = {
            'email': user['email'],
            'nama': user['nama'],
            'is_verified': user['is_verified'],
            'kota_asal': user['kota_asal'],
            'gender': user['gender'],
            'tempat_lahir': user['tempat_lahir'],
            'tanggal_lahir': user['tanggal_lahir'].isoformat() if user['tanggal_lahir'] else None,
            'is_premium': is_premium,
            'is_artist': 'artist' in user_roles,
            'is_songwriter': 'songwriter' in user_roles,
            'is_podcaster': 'podcaster' in user_roles,
            'is_label': False,
            'subscription': subscription_info
        }
        
        # Add role-specific data
        # Always get user playlists for all users (except labels)
        playlist_query = """
            SELECT up.id_user_playlist, up.judul, up.deskripsi, up.jumlah_lagu, 
                   up.tanggal_dibuat, up.total_durasi
            FROM USER_PLAYLIST up
            WHERE up.email_pembuat = %s
            ORDER BY up.tanggal_dibuat DESC
        """
        playlists = fetch_all(playlist_query, [user_email])
        
        dashboard_data['playlists'] = []
        for playlist in playlists:
            dashboard_data['playlists'].append({
                'id': str(playlist['id_user_playlist']),
                'judul': playlist['judul'],
                'deskripsi': playlist['deskripsi'],
                'jumlah_lagu': playlist['jumlah_lagu'],
                'tanggal_dibuat': playlist['tanggal_dibuat'].isoformat(),
                'total_durasi': playlist['total_durasi']
            })
        
        # Initialize empty arrays for all users
        dashboard_data['songs'] = []
        dashboard_data['albums'] = []
        dashboard_data['podcasts'] = []
        
        if 'artist' in user_roles or 'songwriter' in user_roles:
            # Get songs for artists/songwriters
            if 'artist' in user_roles:
                songs_query = """
                    SELECT k.id, k.judul, k.tanggal_rilis, k.durasi, s.total_play, s.total_download,
                           al.judul as album_judul
                    FROM KONTEN k
                    JOIN SONG s ON k.id = s.id_konten
                    JOIN ARTIST a ON s.id_artist = a.id
                    JOIN ALBUM al ON s.id_album = al.id
                    WHERE a.email_akun = %s
                    ORDER BY k.tanggal_rilis DESC
                """
                songs = fetch_all(songs_query, [user_email])
                
                # Get albums for artists
                albums_query = """
                    SELECT DISTINCT al.id, al.judul, al.jumlah_lagu, al.total_durasi,
                           (SELECT MIN(k.tanggal_rilis) 
                            FROM KONTEN k 
                            JOIN SONG s ON k.id = s.id_konten 
                            WHERE s.id_album = al.id) as tanggal_rilis
                    FROM ALBUM al
                    JOIN SONG s ON al.id = s.id_album
                    JOIN ARTIST a ON s.id_artist = a.id
                    WHERE a.email_akun = %s
                    ORDER BY tanggal_rilis DESC
                """
                albums = fetch_all(albums_query, [user_email])
            else:
                # Songwriter
                songs_query = """
                    SELECT k.id, k.judul, k.tanggal_rilis, k.durasi, s.total_play, s.total_download,
                           al.judul as album_judul
                    FROM KONTEN k
                    JOIN SONG s ON k.id = s.id_konten
                    JOIN SONGWRITER_WRITE_SONG sws ON s.id_konten = sws.id_song
                    JOIN SONGWRITER sw ON sws.id_songwriter = sw.id
                    JOIN ALBUM al ON s.id_album = al.id
                    WHERE sw.email_akun = %s
                    ORDER BY k.tanggal_rilis DESC
                """
                songs = fetch_all(songs_query, [user_email])
                
                # Get albums for songwriters (albums that contain songs they wrote)
                albums_query = """
                    SELECT DISTINCT al.id, al.judul, al.jumlah_lagu, al.total_durasi,
                           (SELECT MIN(k.tanggal_rilis) 
                            FROM KONTEN k 
                            JOIN SONG s ON k.id = s.id_konten 
                            WHERE s.id_album = al.id) as tanggal_rilis
                    FROM ALBUM al
                    JOIN SONG s ON al.id = s.id_album
                    JOIN SONGWRITER_WRITE_SONG sws ON s.id_konten = sws.id_song
                    JOIN SONGWRITER sw ON sws.id_songwriter = sw.id
                    WHERE sw.email_akun = %s
                    ORDER BY tanggal_rilis DESC
                """
                albums = fetch_all(albums_query, [user_email])
            
            # Update songs array (already initialized)
            for song in songs:
                dashboard_data['songs'].append({
                    'id': str(song['id']),
                    'judul': song['judul'],
                    'album': song['album_judul'],
                    'tanggal_rilis': song['tanggal_rilis'].isoformat(),
                    'durasi': song['durasi'],
                    'total_play': song['total_play'],
                    'total_download': song['total_download']
                })
            
            # Update albums array (already initialized)
            for album in albums:
                dashboard_data['albums'].append({
                    'id': str(album['id']),
                    'judul': album['judul'],
                    'jumlah_lagu': album['jumlah_lagu'],
                    'total_durasi': album['total_durasi'],
                    'tanggal_rilis': album['tanggal_rilis'].isoformat() if album['tanggal_rilis'] else None
                })
        
        if 'podcaster' in user_roles:
            # Get podcasts for podcasters
            podcasts_query = """
                SELECT k.id, k.judul, k.tanggal_rilis, k.durasi,
                       COUNT(e.id_episode) as jumlah_episode
                FROM KONTEN k
                JOIN PODCAST p ON k.id = p.id_konten
                LEFT JOIN EPISODE e ON p.id_konten = e.id_konten_podcast
                WHERE p.email_podcaster = %s
                GROUP BY k.id, k.judul, k.tanggal_rilis, k.durasi
                ORDER BY k.tanggal_rilis DESC
            """
            podcasts = fetch_all(podcasts_query, [user_email])
            
            # Update podcasts array (already initialized)
            for podcast in podcasts:
                dashboard_data['podcasts'].append({
                    'id': str(podcast['id']),
                    'judul': podcast['judul'],
                    'tanggal_rilis': podcast['tanggal_rilis'].isoformat(),
                    'durasi': podcast['durasi'],
                    'jumlah_episode': podcast['jumlah_episode'] or 0
                })
        
        return Response(dashboard_data)
        
    except Exception as e:
        return Response({
            'error': f'Terjadi kesalahan: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def get_label_dashboard(user_email):
    """Get dashboard for labels"""
    try:
        # Get basic label info
        label_query = """
            SELECT id, nama, email, kontak
            FROM LABEL 
            WHERE email = %s
        """
        label = fetch_one(label_query, [user_email])
        
        if not label:
            return Response({
                'error': 'Label tidak ditemukan'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Get albums under this label
        albums_query = """
            SELECT a.id, a.judul, a.jumlah_lagu, a.total_durasi, 
                   COUNT(s.id_konten) as total_songs
            FROM ALBUM a
            LEFT JOIN SONG s ON a.id = s.id_album
            WHERE a.id_label = %s
            GROUP BY a.id, a.judul, a.jumlah_lagu, a.total_durasi
            ORDER BY a.judul
        """
        albums = fetch_all(albums_query, [label['id']])
        
        # Get total royalties for the label
        royalty_query = """
            SELECT COALESCE(SUM(r.jumlah), 0) as total_royalty
            FROM ROYALTI r
            JOIN SONG s ON r.id_song = s.id_konten
            JOIN ALBUM a ON s.id_album = a.id
            WHERE a.id_label = %s
        """
        royalty_result = fetch_one(royalty_query, [label['id']])
        total_royalty = royalty_result['total_royalty'] if royalty_result else 0
        
        dashboard_data = {
            'email': label['email'],
            'nama': label['nama'],
            'kontak': label['kontak'],
            'albums': [],
            'total_royalty': float(total_royalty)
        }
        
        for album in albums:
            dashboard_data['albums'].append({
                'id': str(album['id']),
                'judul': album['judul'],
                'jumlah_lagu': album['jumlah_lagu'],
                'total_durasi': album['total_durasi'],
                'total_songs': album['total_songs'] or 0
            })
        
        return Response(dashboard_data)
        
    except Exception as e:
        return Response({
            'error': f'Terjadi kesalahan: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@require_authentication
def user_stats(request):
    """
    Get user statistics
    GET /api/dashboard/stats/
    """
    try:
        user_email = request.user_email
        user_roles = request.user_roles
        
        stats = {}
        
        if 'user' in user_roles:
            # Get playlist count
            playlist_count_query = """
                SELECT COUNT(*) as count
                FROM USER_PLAYLIST
                WHERE email_pembuat = %s
            """
            playlist_count = fetch_one(playlist_count_query, [user_email])
            stats['playlists'] = playlist_count['count'] if playlist_count else 0
        
        if 'artist' in user_roles or 'songwriter' in user_roles:
            # Get song count and total plays
            if 'artist' in user_roles:
                song_stats_query = """
                    SELECT COUNT(*) as song_count, COALESCE(SUM(s.total_play), 0) as total_plays
                    FROM SONG s
                    JOIN ARTIST a ON s.id_artist = a.id
                    WHERE a.email_akun = %s
                """
            else:
                song_stats_query = """
                    SELECT COUNT(*) as song_count, COALESCE(SUM(s.total_play), 0) as total_plays
                    FROM SONG s
                    JOIN SONGWRITER_WRITE_SONG sws ON s.id_konten = sws.id_song
                    JOIN SONGWRITER sw ON sws.id_songwriter = sw.id
                    WHERE sw.email_akun = %s
                """
            
            song_stats = fetch_one(song_stats_query, [user_email])
            stats['songs'] = song_stats['song_count'] if song_stats else 0
            stats['total_plays'] = song_stats['total_plays'] if song_stats else 0
        
        if 'podcaster' in user_roles:
            # Get podcast count
            podcast_count_query = """
                SELECT COUNT(*) as count
                FROM PODCAST
                WHERE email_podcaster = %s
            """
            podcast_count = fetch_one(podcast_count_query, [user_email])
            stats['podcasts'] = podcast_count['count'] if podcast_count else 0
        
        return Response(stats)
        
    except Exception as e:
        return Response({
            'error': f'Terjadi kesalahan: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)