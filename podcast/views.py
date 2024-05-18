from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render
from play_podcast.views import convert_duration
from utils.query import connectdb
from django.urls import reverse
from django.db.backends.utils import CursorWrapper
from uuid import uuid4
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.http import JsonResponse

@connectdb
def daftar_podcast(cursor: CursorWrapper, request):
    email = request.session.get('email')
    is_podcaster = request.session.get('is_podcaster', False)
    is_artist = request.session.get('is_artist', False)
    is_songwriter = request.session.get('is_songwriter', False)
    is_podcaster = request.session.get('is_podcaster', False)
    status_langganan = request.session.get('status_langganan', 'Non-Premium')
    
    cursor.execute("""
        SELECT p.id_konten AS podcast_id, k.judul AS podcast_title, a.nama AS podcaster_name,
               k.durasi AS total_duration, COUNT(e.id_episode) AS episode_count
        FROM PODCAST p
        JOIN KONTEN k ON p.id_konten = k.id
        LEFT JOIN EPISODE e ON p.id_konten = e.id_konten_podcast
        LEFT JOIN PODCASTER po ON p.email_podcaster = po.email
        LEFT JOIN AKUN a ON po.email = a.email
        WHERE po.email = %s
        GROUP BY p.id_konten, k.judul, a.nama, k.durasi
        ORDER BY k.judul;
    """, (email,))
    
    podcast_data = cursor.fetchall()

    podcasts = []
    for row in podcast_data:
        podcast = {
            'id': row[0],
            'title': row[1],
            'podcaster_name': row[2],
            'total_duration': convert_duration(row[3]),
            'episode_count': row[4]
        }
        podcasts.append(podcast)
   
    cursor.execute("SELECT DISTINCT genre FROM Genre;")
    genres = [row[0] for row in cursor.fetchall()]
    
    content = {
        'podcasts': podcasts,
        'status_langganan': status_langganan,
        'isArtist': is_artist,
        'isSongwriter': is_songwriter,
        'isPodcaster': is_podcaster,
        'genres': genres 
    }
    
    return render(request, 'podcast.html', content)


@connectdb
def daftar_episode(cursor: CursorWrapper, request):
    podcast_name = request.GET.get('podcast')

    if not podcast_name:
        return HttpResponseNotFound('Podcast not found.')

    cursor.execute("""
        SELECT id
        FROM KONTEN
        WHERE judul = %s;
    """, (podcast_name,))
    
    row = cursor.fetchone()

    if not row:
        return HttpResponseNotFound('Podcast not found.')

    podcast_id = row[0]

    cursor.execute("""
        SELECT id_episode, judul, deskripsi, tanggal_rilis, durasi
        FROM EPISODE
        WHERE id_konten_podcast = %s
        ORDER BY tanggal_rilis;
    """, (podcast_id,))
    
    episodes_data = cursor.fetchall()

    episodes = []
    for episode in episodes_data:
        episode_data = {
            'id': episode[0],
            'title': episode[1],
            'description': episode[2],
            'release_date': episode[3],
            'duration': convert_duration(episode[4])
        }
        episodes.append(episode_data)

    content = {
        'podcast_name': podcast_name,
        'episodes': episodes,
    }

    return render(request, 'episode.html', content)

@connectdb
@csrf_exempt
def add_podcast(cursor: CursorWrapper, request):
    if request.method == 'POST':
        email = request.session.get('email')
        podcast_title = request.POST.get("title")
        podcast_genre = request.POST.get("genre")
        id_konten = str(uuid4())
        tanggal_rilis = str(datetime.now().date())
        tahun = datetime.now().year
        total_durasi = 0
        
        # Masukkan data ke dalam tabel KONTEN
        cursor.execute("""
            INSERT INTO KONTEN (id, judul, tanggal_rilis, tahun, durasi)
            VALUES (%s, %s, %s, %s, %s);
        """, (id_konten, podcast_title, tanggal_rilis, tahun, total_durasi))

        # Masukkan data ke dalam tabel GENRE
        cursor.execute("""
            INSERT INTO GENRE (id_konten, genre)
            VALUES (%s, %s);
        """, (id_konten, podcast_genre))

        # Masukkan data ke dalam tabel PODCAST
        cursor.execute("""
            INSERT INTO PODCAST (id_konten, email_podcaster)
            VALUES (%s, %s);
        """, (id_konten, email))

        
        return HttpResponse(b"CREATED", status=201)

    return HttpResponseNotFound()

@connectdb
@csrf_exempt
def remove_podcast(cursor: CursorWrapper, request):
    if request.method == 'POST':
        podcastID = request.POST.get("id")
        # print("podcast id: " + podcastID)
        
        # Query SQL untuk menghapus data konten dari tabel konten
        query = """
        DELETE FROM KONTEN
        WHERE id = %s;
        """

        cursor.execute(query, (podcastID,))
        
        return HttpResponse(b"DELETED", status=204)

    return HttpResponseNotFound()


@connectdb
@csrf_exempt
def add_episode(cursor: CursorWrapper, request):
    if request.method == 'POST':
        podcast_id = request.POST.get("pod_id")
        episode_title = request.POST.get("ep_title")
        episode_duration = int(request.POST.get("ep_duration")) * 60
        episode_description = request.POST.get("ep_description")
        id_episode = str(uuid4())
        tanggal_rilis = str(datetime.now().date())
        
        cursor.execute("""
            INSERT INTO EPISODE (id_episode, id_konten_podcast, judul, deskripsi, durasi, tanggal_rilis)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (id_episode, podcast_id, episode_title, episode_description, episode_duration, tanggal_rilis))
        
        return HttpResponse(b"CREATED", status=201)
 

    return HttpResponseNotFound()

@connectdb
@csrf_exempt
def remove_episode(cursor: CursorWrapper, request):
    if request.method == 'POST':
        episode_id = request.POST.get("episode_id")
        
        # Query SQL untuk menghapus data konten dari tabel konten
        query = """
        DELETE FROM EPISODE
        WHERE id_episode = %s;
        """

        cursor.execute(query, (episode_id,))
        
        
        return HttpResponse(b"DELETED", status=204)

    return HttpResponseNotFound()