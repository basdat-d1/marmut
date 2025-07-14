from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from utils.authentication import require_authentication
from utils.database import execute_query, execute_single_query, fetch_all

@api_view(['GET'])
@require_authentication
def search(request):
    try:
        query = request.GET.get('q', '').strip()
        
        if not query:
            return Response({
                'error': 'Query pencarian harus diisi'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        results = {
            'query': query,
            'songs': [],
            'podcasts': [],
            'playlists': [],
            'total': 0
        }
        
        # Search songs (by title, artist, genre)
        songs_query = """
            SELECT DISTINCT k.id, k.judul, a.nama as artist_nama, k.durasi, s.total_play
            FROM KONTEN k
            JOIN SONG s ON k.id = s.id_konten
            JOIN ARTIST ar ON s.id_artist = ar.id
            JOIN AKUN a ON ar.email_akun = a.email
            LEFT JOIN GENRE g ON k.id = g.id_konten
            WHERE LOWER(k.judul) LIKE LOWER(%s)
               OR LOWER(a.nama) LIKE LOWER(%s)
               OR LOWER(g.genre) LIKE LOWER(%s)
            ORDER BY s.total_play DESC, k.judul
        """
        songs = fetch_all(songs_query, [f'%{query}%', f'%{query}%', f'%{query}%'])
        
        for song in songs:
            results['songs'].append({
                'id': str(song['id']),
                'tipe': 'SONG',
                'judul': song['judul'],
                'oleh': song['artist_nama'],
                'durasi': song['durasi'],
                'total_play': song['total_play']
            })
        
        # Search podcasts (by title, podcaster, genre)
        podcasts_query = """
            SELECT DISTINCT k.id, k.judul, a.nama as podcaster_nama, k.durasi,
                   COUNT(e.id_episode) as jumlah_episode
            FROM KONTEN k
            JOIN PODCAST p ON k.id = p.id_konten
            JOIN AKUN a ON p.email_podcaster = a.email
            LEFT JOIN EPISODE e ON p.id_konten = e.id_konten_podcast
            LEFT JOIN GENRE g ON k.id = g.id_konten
            WHERE LOWER(k.judul) LIKE LOWER(%s)
               OR LOWER(a.nama) LIKE LOWER(%s)
               OR LOWER(g.genre) LIKE LOWER(%s)
            GROUP BY k.id, k.judul, a.nama, k.durasi
            ORDER BY k.judul
        """
        podcasts = fetch_all(podcasts_query, [f'%{query}%', f'%{query}%', f'%{query}%'])
        
        for podcast in podcasts:
            results['podcasts'].append({
                'id': str(podcast['id']),
                'tipe': 'PODCAST',
                'judul': podcast['judul'],
                'oleh': podcast['podcaster_nama'],
                'durasi': podcast['durasi'],
                'jumlah_episode': podcast['jumlah_episode'] or 0
            })
        
        # Search user playlists (by title, creator)
        playlists_query = """
            SELECT up.id_user_playlist, up.judul, a.nama as pembuat_nama, 
                   up.jumlah_lagu, up.total_durasi
            FROM USER_PLAYLIST up
            JOIN AKUN a ON up.email_pembuat = a.email
            WHERE LOWER(up.judul) LIKE LOWER(%s)
               OR LOWER(a.nama) LIKE LOWER(%s)
            ORDER BY up.judul
        """
        playlists = fetch_all(playlists_query, [f'%{query}%', f'%{query}%'])
        
        for playlist in playlists:
            results['playlists'].append({
                'id': str(playlist['id_user_playlist']),
                'tipe': 'USER_PLAYLIST',
                'judul': playlist['judul'],
                'oleh': playlist['pembuat_nama'],
                'jumlah_lagu': playlist['jumlah_lagu'],
                'total_durasi': playlist['total_durasi']
            })
        
        # Calculate total results
        results['total'] = len(results['songs']) + len(results['podcasts']) + len(results['playlists'])
        
        if results['total'] == 0:
            return Response({
                'message': f'Maaf, pencarian untuk "{query}" tidak ditemukan',
                'query': query,
                'results': results
            })
        
        return Response({
            'message': f'Ditemukan {results["total"]} hasil untuk "{query}"',
            'query': query,
            'results': results
        })
        
    except Exception as e:
        return Response({
            'error': f'Terjadi kesalahan: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@require_authentication
def search_songs(request):
    try:
        query = request.GET.get('q', '').strip()
        
        if not query:
            return Response({
                'error': 'Query pencarian harus diisi'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        songs_query = """
            SELECT k.id, k.judul, a.nama as artist_nama, k.durasi, s.total_play, s.total_download,
                   al.judul as album_nama
            FROM KONTEN k
            JOIN SONG s ON k.id = s.id_konten
            JOIN ARTIST ar ON s.id_artist = ar.id
            JOIN AKUN a ON ar.email_akun = a.email
            JOIN ALBUM al ON s.id_album = al.id
            WHERE LOWER(k.judul) LIKE LOWER(%s) OR LOWER(a.nama) LIKE LOWER(%s)
            ORDER BY s.total_play DESC, k.judul
        """
        songs = fetch_all(songs_query, [f'%{query}%', f'%{query}%'])
        
        song_data = []
        for song in songs:
            song_data.append({
                'id': str(song['id']),
                'judul': song['judul'],
                'artist': song['artist_nama'],
                'album': song['album_nama'],
                'durasi': song['durasi'],
                'total_play': song['total_play'],
                'total_download': song['total_download']
            })
        
        return Response({
            'query': query,
            'songs': song_data,
            'total': len(song_data)
        })
        
    except Exception as e:
        return Response({
            'error': f'Terjadi kesalahan: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@require_authentication
def search_podcasts(request):
    try:
        query = request.GET.get('q', '').strip()
        
        if not query:
            return Response({
                'error': 'Query pencarian harus diisi'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        podcasts_query = """
            SELECT k.id, k.judul, a.nama as podcaster_nama, k.durasi, k.tanggal_rilis,
                   COUNT(e.id_episode) as jumlah_episode
            FROM KONTEN k
            JOIN PODCAST p ON k.id = p.id_konten
            JOIN AKUN a ON p.email_podcaster = a.email
            LEFT JOIN EPISODE e ON p.id_konten = e.id_konten_podcast
            WHERE LOWER(k.judul) LIKE LOWER(%s) OR LOWER(a.nama) LIKE LOWER(%s)
            GROUP BY k.id, k.judul, a.nama, k.durasi, k.tanggal_rilis
            ORDER BY k.tanggal_rilis DESC, k.judul
        """
        podcasts = fetch_all(podcasts_query, [f'%{query}%', f'%{query}%'])
        
        podcast_data = []
        for podcast in podcasts:
            podcast_data.append({
                'id': str(podcast['id']),
                'judul': podcast['judul'],
                'podcaster': podcast['podcaster_nama'],
                'durasi': podcast['durasi'],
                'tanggal_rilis': podcast['tanggal_rilis'].isoformat(),
                'jumlah_episode': podcast['jumlah_episode'] or 0
            })
        
        return Response({
            'query': query,
            'podcasts': podcast_data,
            'total': len(podcast_data)
        })
        
    except Exception as e:
        return Response({
            'error': f'Terjadi kesalahan: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@require_authentication
def search_playlists(request):
    try:
        query = request.GET.get('q', '').strip()
        
        if not query:
            return Response({
                'error': 'Query pencarian harus diisi'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        playlists_query = """
            SELECT up.id_user_playlist, up.judul, a.nama as pembuat_nama, 
                   up.jumlah_lagu, up.total_durasi, up.tanggal_dibuat, up.deskripsi
            FROM USER_PLAYLIST up
            JOIN AKUN a ON up.email_pembuat = a.email
            WHERE LOWER(up.judul) LIKE LOWER(%s) OR LOWER(a.nama) LIKE LOWER(%s)
            ORDER BY up.tanggal_dibuat DESC, up.judul
        """
        playlists = fetch_all(playlists_query, [f'%{query}%', f'%{query}%'])
        
        playlist_data = []
        for playlist in playlists:
            # Format duration
            durasi_menit = playlist['total_durasi']
            if durasi_menit >= 60:
                jam = durasi_menit // 60
                menit = durasi_menit % 60
                durasi_str = f"{jam} jam {menit} menit"
            else:
                durasi_str = f"{durasi_menit} menit"
            
            playlist_data.append({
                'id': str(playlist['id_user_playlist']),
                'judul': playlist['judul'],
                'pembuat': playlist['pembuat_nama'],
                'deskripsi': playlist['deskripsi'],
                'jumlah_lagu': playlist['jumlah_lagu'],
                'total_durasi': durasi_str,
                'tanggal_dibuat': playlist['tanggal_dibuat'].isoformat()
            })
        
        return Response({
            'query': query,
            'playlists': playlist_data,
            'total': len(playlist_data)
        })
        
    except Exception as e:
        return Response({
            'error': f'Terjadi kesalahan: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@require_authentication
def get_item_detail(request, item_id):
    """Get detailed information about a specific item"""
    try:
        item_type = request.GET.get('type', 'song')
        
        if item_type == 'song':
            item = execute_single_query(
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
                [item_id]
            )
            
            if item:
                return Response({
                    'type': 'song',
                    'item': {
                        'id': item['id'],
                        'judul': item['judul'],
                        'artist': item['artist'],
                        'album': item['album_judul'],
                        'durasi': item['durasi'],
                        'tanggal_rilis': item['tanggal_rilis'],
                        'tahun': item['tahun'],
                        'genres': item['genres'] or [],
                        'total_play': item['total_play'],
                        'total_download': item['total_download']
                    }
                }, status=status.HTTP_200_OK)
                
        elif item_type == 'album':
            item = execute_single_query(
                """SELECT a.id, a.judul, l.nama as label, a.jumlah_lagu, a.total_durasi
                   FROM ALBUM a
                   JOIN LABEL l ON a.id_label = l.id
                   WHERE a.id = %s""",
                [item_id]
            )
            
            if item:
                # Get album songs
                songs = execute_query(
                    """SELECT k.id, k.judul, ak.nama as artist, k.durasi
                       FROM SONG s
                       JOIN KONTEN k ON s.id_konten = k.id
                       JOIN ARTIST ar ON s.id_artist = ar.id
                       JOIN AKUN ak ON ar.email_akun = ak.email
                       WHERE s.id_album = %s
                       ORDER BY k.judul""",
                    [item_id]
                )
                
                return Response({
                    'type': 'album',
                    'item': {
                        'id': item['id'],
                        'judul': item['judul'],
                        'label': item['label'],
                        'jumlah_lagu': item['jumlah_lagu'],
                        'total_durasi': item['total_durasi'],
                        'songs': [
                            {
                                'id': song['id'],
                                'judul': song['judul'],
                                'artist': song['artist'],
                                'durasi': song['durasi']
                            } for song in songs
                        ]
                    }
                }, status=status.HTTP_200_OK)
                
        elif item_type == 'podcast':
            item = execute_single_query(
                """SELECT k.id, k.judul, ak.nama as podcaster, k.durasi
        FROM KONTEN k
                   JOIN PODCAST p ON k.id = p.id_konten
                   JOIN AKUN ak ON p.email_podcaster = ak.email
                   WHERE k.id = %s""",
                [item_id]
            )
            
            if item:
                # Get podcast episodes
                episodes = execute_query(
                    """SELECT k.id, k.judul, k.durasi, e.deskripsi
                       FROM EPISODE e
                       JOIN KONTEN k ON e.id_konten = k.id
                       WHERE e.id_konten_podcast = %s
                       ORDER BY k.tanggal_rilis DESC""",
                    [item_id]
                )
                
                return Response({
                    'type': 'podcast',
                    'item': {
                        'id': item['id'],
                        'judul': item['judul'],
                        'podcaster': item['podcaster'],
                        'durasi': item['durasi'],
                        'episodes': [
                            {
                                'id': episode['id'],
                                'judul': episode['judul'],
                                'deskripsi': episode['deskripsi'],
                                'durasi': episode['durasi']
                            } for episode in episodes
                        ]
                    }
                }, status=status.HTTP_200_OK)
                
        elif item_type == 'playlist':
            item = execute_single_query(
                """SELECT up.id_user_playlist, up.judul, ak.nama as creator, 
                          up.deskripsi, up.jumlah_lagu, up.total_durasi
        FROM USER_PLAYLIST up
        JOIN AKUN ak ON up.email_pembuat = ak.email
                   WHERE up.id_user_playlist = %s""",
                [item_id]
            )
            
            if item:
                # Get playlist songs
                songs = execute_query(
                    """SELECT k.id, k.judul, ak.nama as artist, k.durasi
                       FROM PLAYLIST_SONG ps
                       JOIN USER_PLAYLIST up ON ps.id_playlist = up.id_playlist
                       JOIN SONG s ON ps.id_song = s.id_konten
                       JOIN KONTEN k ON s.id_konten = k.id
                       JOIN ARTIST ar ON s.id_artist = ar.id
                       JOIN AKUN ak ON ar.email_akun = ak.email
        WHERE up.id_user_playlist = %s
                       ORDER BY k.judul""",
                    [item_id]
                )
                
                return Response({
                    'type': 'playlist',
                    'item': {
                        'id': item['id_user_playlist'],
                        'judul': item['judul'],
                        'creator': item['creator'],
                        'deskripsi': item['deskripsi'],
                        'jumlah_lagu': item['jumlah_lagu'],
                        'total_durasi': item['total_durasi'],
                        'songs': [
                            {
                                'id': song['id'],
                                'judul': song['judul'],
                                'artist': song['artist'],
                                'durasi': song['durasi']
                            } for song in songs
                        ]
                    }
                }, status=status.HTTP_200_OK)
        
        return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)