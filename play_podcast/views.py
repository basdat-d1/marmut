from datetime import datetime
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from utils.authentication import require_authentication
from utils.database import execute_query, execute_single_query, execute_insert_query

def convert_duration(minutes):
    """Convert minutes to format: _ jam _ menit"""
    hours = minutes // 60
    mins = minutes % 60
    if hours > 0 and mins > 0:
        return f"{hours} jam {mins} menit"
    elif hours > 0:
        return f"{hours} jam"
    else:
        return f"{mins} menit"

@api_view(['GET'])
@require_authentication
def get_podcast_detail(request, podcast_id):
    """Get podcast details with episodes"""
    try:
        # Get podcast details
        podcast = execute_single_query(
            """SELECT p.id_konten, k.judul, k.durasi, k.tanggal_rilis,
                      ak.nama as podcaster_name, po.email as podcaster_email
               FROM PODCAST p
               JOIN KONTEN k ON p.id_konten = k.id
               JOIN PODCASTER po ON p.email_podcaster = po.email
               JOIN AKUN ak ON po.email = ak.email
               WHERE p.id_konten = %s""",
            [podcast_id]
        )
        
        if not podcast:
            return Response({'error': 'Podcast not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Get podcast episodes
        episodes = execute_query(
            """SELECT e.id_episode, e.judul, e.deskripsi, e.durasi, e.tanggal_rilis
               FROM EPISODE e
               WHERE e.id_konten_podcast = %s
               ORDER BY e.tanggal_rilis DESC""",
            [podcast_id]
        )
        
        # Get podcast genres
        genres = execute_query(
            """SELECT g.genre
               FROM GENRE g
               WHERE g.id_konten = %s""",
            [podcast_id]
        )
        
        return Response({
            'podcast': {
                'id': podcast['id_konten'],
                'judul': podcast['judul'],
                'total_durasi': convert_duration(podcast['durasi']),
                'tanggal_rilis': podcast['tanggal_rilis'],
                'podcaster': podcast['podcaster_name'],
                'podcaster_email': podcast['podcaster_email'],
                'genres': [genre['genre'] for genre in genres]
            },
            'episodes': [
                {
                    'id': episode['id_episode'],
                    'judul': episode['judul'],
                    'deskripsi': episode['deskripsi'],
                    'durasi': convert_duration(episode['durasi']),
                    'tanggal_rilis': episode['tanggal_rilis']
                } for episode in episodes
            ]
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@require_authentication
def play_podcast_episode(request, podcast_id, episode_id):
    """Play a specific podcast episode"""
    try:
        email = request.session.get('email')
        if not email:
            return Response({'error': 'Not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Verify episode exists
        episode = execute_single_query(
            """SELECT e.id_episode, e.judul, e.durasi
               FROM EPISODE e
               WHERE e.id_episode = %s AND e.id_konten_podcast = %s""",
            [episode_id, podcast_id]
        )
        
        if not episode:
            return Response({'error': 'Episode not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Record episode play
        timestamp = datetime.now()
        execute_insert_query(
            """INSERT INTO AKUN_PLAY_EPISODE (email_pemain, id_episode, waktu)
               VALUES (%s, %s, %s)""",
            [email, episode_id, timestamp]
        )
        
        return Response({
            'message': 'Episode played successfully',
            'episode': {
                'id': episode['id_episode'],
                'judul': episode['judul'],
                'durasi': convert_duration(episode['durasi'])
            },
            'timestamp': timestamp
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@require_authentication
def get_all_podcasts(request):
    """Get all podcasts"""
    try:
        podcasts = execute_query(
            """SELECT p.id_konten, k.judul, k.durasi, k.tanggal_rilis,
                      ak.nama as podcaster_name,
                      COUNT(e.id_episode) as episode_count
    FROM PODCAST p
    JOIN KONTEN k ON p.id_konten = k.id
               JOIN PODCASTER po ON p.email_podcaster = po.email
               JOIN AKUN ak ON po.email = ak.email
    LEFT JOIN EPISODE e ON p.id_konten = e.id_konten_podcast
               GROUP BY p.id_konten, k.judul, k.durasi, k.tanggal_rilis, ak.nama
               ORDER BY k.tanggal_rilis DESC""",
            []
        )
        
        return Response({
            'podcasts': [
                {
                    'id': podcast['id_konten'],
                    'judul': podcast['judul'],
                    'podcaster': podcast['podcaster_name'],
                    'total_durasi': convert_duration(podcast['durasi']),
                    'episode_count': podcast['episode_count'],
                    'tanggal_rilis': podcast['tanggal_rilis']
                } for podcast in podcasts
            ]
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
