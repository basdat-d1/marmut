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
    query = """
    SELECT p.id_konten AS podcast_id, k.judul AS podcast_title, 
           e.id_episode, e.judul AS episode_title, e.deskripsi, e.durasi AS episode_duration, e.tanggal_rilis AS episode_release_date,
           g.genre, a.nama AS podcaster_name
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
                "total_duration": 0,
                "episodes": [],
                "genres": set(),
                "podcaster": row[8]
            }
        if row[2]: 
            episode_duration = row[5] if row[5] else 0
            podcasts_dict[podcast_id]["total_duration"] += episode_duration
            podcasts_dict[podcast_id]["episodes"].append({
                "judul": row[3],
                "deskripsi": row[4],
                "durasi_episode": convert_duration(episode_duration),
                "tanggal_episode": row[6]
            })
        if row[7]:
            podcasts_dict[podcast_id]["genres"].add(row[7])

    for podcast_id in podcasts_dict:
        podcasts_dict[podcast_id]["total_duration"] = convert_duration(podcasts_dict[podcast_id]["total_duration"])
        podcasts_dict[podcast_id]["genres"] = ", ".join(podcasts_dict[podcast_id]["genres"])

    content = {
        "podcasts": list(podcasts_dict.values())
    }

    return render(request, 'play_podcast.html', content)