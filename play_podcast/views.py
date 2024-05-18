from django.shortcuts import render
from utils.query import connectdb
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.db.backends.utils import CursorWrapper

def convert_duration(minutes):
    hours = minutes // 60
    mins = minutes % 60
    if hours > 0 and mins > 0:
        return f"{hours} hour {mins} minutes"
    elif hours > 0:
        return f"{hours} hour"
    else:
        return f"{mins} minutes"

@connectdb
def show_podcast(cursor: CursorWrapper, request):
    is_podcaster = request.session.get('is_podcaster')
    is_artist = request.session.get('is_artist')
    is_songwriter = request.session.get('is_songwriter')
    status_langganan = request.session.get('is_premium')
    
    query = """
    SELECT p.id_konten AS podcast_id, k.judul AS podcast_title, k.durasi AS total_duration,
           e.id_episode, e.judul AS episode_title, e.deskripsi, e.durasi AS episode_duration, e.tanggal_rilis AS episode_release_date,
           g.genre, a.nama AS podcaster_name, k.tanggal_rilis AS podcast_release_date
    FROM PODCAST p
    JOIN KONTEN k ON p.id_konten = k.id
    LEFT JOIN EPISODE e ON p.id_konten = e.id_konten_podcast
    LEFT JOIN GENRE g ON k.id = g.id_konten
    LEFT JOIN PODCASTER po ON p.email_podcaster = po.email
    LEFT JOIN AKUN a ON po.email = a.email
    ORDER BY k.judul, e.tanggal_rilis;
    """
    cursor.execute(query)
    rows = cursor.fetchall()

    podcasts_dict = {}
    for row in rows:
        podcast_id = row[0]
        if podcast_id not in podcasts_dict:
            podcasts_dict[podcast_id] = {
                "title": row[1],
                "total_duration": convert_duration(row[2]),
                "podcast_release_date": row[10],  # Menambahkan tanggal rilis podcast
                "episodes": [],
                "genres": set(),
                "podcaster": row[9]
            }
        if row[3]: 
            podcasts_dict[podcast_id]["episodes"].append({
                "judul": row[4],
                "deskripsi": row[5],
                "durasi_episode": convert_duration(row[6]),
                "tanggal_episode": row[7]
            })
        if row[8]:
            podcasts_dict[podcast_id]["genres"].add(row[8])

    for podcast_id in podcasts_dict:
        podcasts_dict[podcast_id]["genres"] = ", ".join(podcasts_dict[podcast_id]["genres"])

    content = {
        "podcasts": list(podcasts_dict.values()),
        'status_langganan': status_langganan,
        'isArtist': is_artist,
        'isSongwriter': is_songwriter,
        'isPodcaster': is_podcaster,
    }

    return render(request, 'play_podcast.html', content)
