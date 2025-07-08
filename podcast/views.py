from datetime import datetime
from uuid import uuid4
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from utils.authentication import require_authentication
from utils.database import execute_query, execute_single_query, execute_insert_query, execute_delete_query

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
def get_user_podcasts(request):
    """Get podcasts created by the authenticated user"""
    try:
        email = request.user_email
        if not email:
            return Response({'error': 'Not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Check if user is a podcaster
        podcaster = execute_single_query(
            "SELECT email FROM PODCASTER WHERE email = %s",
            [email]
        )
        
        if not podcaster:
            return Response({'error': 'User is not a podcaster'}, status=status.HTTP_403_FORBIDDEN)
        
        # Get user's podcasts
        podcasts = execute_query(
            """SELECT p.id_konten, k.judul, k.durasi, k.tanggal_rilis,
                      COUNT(e.id_episode) as episode_count
        FROM PODCAST p
        JOIN KONTEN k ON p.id_konten = k.id
        LEFT JOIN EPISODE e ON p.id_konten = e.id_konten_podcast
               WHERE p.email_podcaster = %s
               GROUP BY p.id_konten, k.judul, k.durasi, k.tanggal_rilis
               ORDER BY k.tanggal_rilis DESC""",
            [email]
        )
        
        return Response({
            'podcasts': [
                {
                    'id': podcast['id_konten'],
                    'judul': podcast['judul'],
                    'total_durasi': convert_duration(podcast['durasi']),
                    'episode_count': podcast['episode_count'],
                    'tanggal_rilis': podcast['tanggal_rilis']
                } for podcast in podcasts
            ]
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@require_authentication
def create_podcast(request):
    """Create a new podcast"""
    try:
        email = request.user_email
        if not email:
            return Response({'error': 'Not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Check if user is a podcaster
        podcaster = execute_single_query(
            "SELECT email FROM PODCASTER WHERE email = %s",
            [email]
        )
        
        if not podcaster:
            return Response({'error': 'User is not a podcaster'}, status=status.HTTP_403_FORBIDDEN)
        
        data = request.data
        podcast_title = data.get('title', '').strip()
        podcast_genre = data.get('genre', '').strip()
        
        if not podcast_title or not podcast_genre:
            return Response({'error': 'Title and genre are required'}, status=status.HTTP_400_BAD_REQUEST)
        
        if podcast_genre == "Select Genre":
            return Response({'error': 'Please select a valid genre'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create podcast
        id_konten = str(uuid4())
        tanggal_rilis = datetime.now().date()
        tahun = datetime.now().year
        total_durasi = 0
        
        # Insert into KONTEN table
        execute_insert_query(
            """INSERT INTO KONTEN (id, judul, tanggal_rilis, tahun, durasi)
               VALUES (%s, %s, %s, %s, %s)""",
            [id_konten, podcast_title, tanggal_rilis, tahun, total_durasi]
        )
        
        # Insert into GENRE table
        execute_insert_query(
            """INSERT INTO GENRE (id_konten, genre)
               VALUES (%s, %s)""",
            [id_konten, podcast_genre]
        )
        
        # Insert into PODCAST table
        execute_insert_query(
            """INSERT INTO PODCAST (id_konten, email_podcaster)
               VALUES (%s, %s)""",
            [id_konten, email]
        )
        
        return Response({
            'message': 'Podcast created successfully',
            'podcast': {
                'id': id_konten,
                'judul': podcast_title,
                'genre': podcast_genre,
                'tanggal_rilis': tanggal_rilis
            }
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
@require_authentication
def delete_podcast(request, podcast_id):
    """Delete a podcast"""
    try:
        email = request.user_email
        if not email:
            return Response({'error': 'Not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Check if user owns the podcast
        podcast = execute_single_query(
            "SELECT email_podcaster FROM PODCAST WHERE id_konten = %s",
            [podcast_id]
        )
        
        if not podcast:
            return Response({'error': 'Podcast not found'}, status=status.HTTP_404_NOT_FOUND)
        
        if podcast['email_podcaster'] != email:
            return Response({'error': 'Unauthorized to delete this podcast'}, status=status.HTTP_403_FORBIDDEN)
        
        # Delete podcast (cascade will handle related records)
        execute_delete_query(
            "DELETE FROM KONTEN WHERE id = %s",
            [podcast_id]
        )
        
        return Response({
            'message': 'Podcast deleted successfully'
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@require_authentication
def get_podcast_episodes(request, podcast_id):
    """Get episodes for a specific podcast"""
    try:
        email = request.user_email
        if not email:
            return Response({'error': 'Not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Check if user owns the podcast
        podcast = execute_single_query(
            """SELECT p.email_podcaster, k.judul
               FROM PODCAST p
               JOIN KONTEN k ON p.id_konten = k.id
               WHERE p.id_konten = %s""",
            [podcast_id]
        )
        
        if not podcast:
            return Response({'error': 'Podcast not found'}, status=status.HTTP_404_NOT_FOUND)
        
        if podcast['email_podcaster'] != email:
            return Response({'error': 'Unauthorized to view episodes'}, status=status.HTTP_403_FORBIDDEN)
        
        # Get episodes
        episodes = execute_query(
            """SELECT id_episode, judul, deskripsi, tanggal_rilis, durasi
               FROM EPISODE
               WHERE id_konten_podcast = %s
               ORDER BY tanggal_rilis DESC""",
            [podcast_id]
        )
        
        return Response({
            'podcast_name': podcast['judul'],
            'episodes': [
                {
                    'id': episode['id_episode'],
                    'judul': episode['judul'],
                    'deskripsi': episode['deskripsi'],
                    'tanggal_rilis': episode['tanggal_rilis'],
                    'durasi': convert_duration(episode['durasi'])
                } for episode in episodes
            ]
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@require_authentication
def create_episode(request, podcast_id):
    """Create a new episode for a podcast"""
    try:
        email = request.session.get('email')
        if not email:
            return Response({'error': 'Not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Check if user owns the podcast
        podcast = execute_single_query(
            "SELECT email_podcaster FROM PODCAST WHERE id_konten = %s",
            [podcast_id]
        )
        
        if not podcast:
            return Response({'error': 'Podcast not found'}, status=status.HTTP_404_NOT_FOUND)
        
        if podcast['email_podcaster'] != email:
            return Response({'error': 'Unauthorized to add episodes'}, status=status.HTTP_403_FORBIDDEN)
        
        data = request.data
        episode_title = data.get('title', '').strip()
        episode_description = data.get('description', '').strip()
        episode_duration_str = data.get('duration', '')
        
        if not episode_title or not episode_description:
            return Response({'error': 'Title and description are required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            episode_duration_minutes = int(episode_duration_str)
            if episode_duration_minutes <= 0:
                raise ValueError()
        except (ValueError, TypeError):
            return Response({'error': 'Duration must be a positive number'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create episode
        id_episode = str(uuid4())
        tanggal_rilis = datetime.now().date()
        episode_duration = episode_duration_minutes * 60  # Convert to seconds
        
        execute_insert_query(
            """INSERT INTO EPISODE (id_episode, id_konten_podcast, judul, deskripsi, durasi, tanggal_rilis)
               VALUES (%s, %s, %s, %s, %s, %s)""",
            [id_episode, podcast_id, episode_title, episode_description, episode_duration, tanggal_rilis]
        )
        
        return Response({
            'message': 'Episode created successfully',
            'episode': {
                'id': id_episode,
                'judul': episode_title,
                'deskripsi': episode_description,
                'durasi': convert_duration(episode_duration),
                'tanggal_rilis': tanggal_rilis
            }
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
@require_authentication
def delete_episode(request, podcast_id, episode_id):
    """Delete an episode"""
    try:
        email = request.session.get('email')
        if not email:
            return Response({'error': 'Not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Check if user owns the podcast
        podcast = execute_single_query(
            "SELECT email_podcaster FROM PODCAST WHERE id_konten = %s",
            [podcast_id]
        )
        
        if not podcast:
            return Response({'error': 'Podcast not found'}, status=status.HTTP_404_NOT_FOUND)
        
        if podcast['email_podcaster'] != email:
            return Response({'error': 'Unauthorized to delete episodes'}, status=status.HTTP_403_FORBIDDEN)
        
        # Check if episode exists
        episode = execute_single_query(
            "SELECT id_episode FROM EPISODE WHERE id_episode = %s AND id_konten_podcast = %s",
            [episode_id, podcast_id]
        )
        
        if not episode:
            return Response({'error': 'Episode not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Delete episode
        execute_delete_query(
            "DELETE FROM EPISODE WHERE id_episode = %s",
            [episode_id]
        )
        
        return Response({
            'message': 'Episode deleted successfully'
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@require_authentication
def get_available_genres(request):
    """Get available podcast genres"""
    try:
        genres = execute_query(
            "SELECT DISTINCT genre FROM GENRE ORDER BY genre",
            []
        )
        
        return Response({
            'genres': [genre['genre'] for genre in genres]
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)