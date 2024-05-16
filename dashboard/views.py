from utils.query import connectdb
from django.urls import reverse
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.db.backends.utils import CursorWrapper

@connectdb
def dashboard_pengguna(cursor: CursorWrapper, request):
    print("masuk dashboard_pengguna")
    try:
        user = request.session.get('email')
    except:
        return HttpResponseRedirect(reverse("authentication:login"))
    
    playlists = ""
    podcasts = ""
    albums = ""
    songs = ""

    cursor.execute("SELECT * FROM AKUN WHERE email = %s", [user])
    user_info = cursor.fetchone()
    
    if (request.session.get('is_podcaster')):
        query =(rf"""SELECT k.judul AS podcast_title, COUNT(e.id_episode) AS episode_count, COALESCE(SUM(e.durasi), 0) AS total_duration_minutes
                FROM podcast AS p
                JOIN konten AS k ON p.id_konten = k.id
                LEFT JOIN episode AS e ON p.id_konten = e.id_konten_podcast
                WHERE p.email_podcaster = '{user}'
                GROUP BY k.judul;
                """)
        cursor.execute(query)
        podcasts = cursor.fetchall()
    if (request.session.get('is_artist')):
        query =(rf"""SELECT KONTEN.judul, SONG.total_play, SONG.total_download
                FROM KONTEN, SONG
                JOIN ARTIST ON SONG.id_artist = ARTIST.id
                WHERE ARTIST.email_akun = '{user}' AND KONTEN.id = SONG.id_konten;
                """)
        cursor.execute(query)
        songs = cursor.fetchall()
    if (request.session.get('is_songwriter')):
        query =(rf"""SELECT konten.judul AS song_title, song.total_play, song.total_download
                FROM royalti
                JOIN song ON royalti.id_song = song.id_konten
                JOIN konten ON song.id_konten = konten.id
                JOIN songwriter ON royalti.id_pemilik_hak_cipta = songwriter.id_pemilik_hak_cipta
                WHERE songwriter.email_akun = '{user}';
                """)
        cursor.execute(query)
        songs = cursor.fetchall()

    query =(rf"""SELECT judul, jumlah_lagu, total_durasi
                FROM user_playlist
                WHERE email_pembuat = '{user}';
                """)
    cursor.execute(query)
    playlists = cursor.fetchall()

    is_artist = request.session.get('is_artist', False)
    is_songwriter = request.session.get('is_songwriter', False)
    is_podcaster = request.session.get('is_podcaster', False)
    status_langganan = request.session.get('status_langganan', 'Non-Premium')
    print( "artist " + str(is_artist))
    print( "songwriter " + str(is_songwriter))
    print( "podcaster " + str(is_podcaster))
    print( "status langganan " + str(status_langganan))

    records_song_artist, records_song_songwriter, records_podcast = [], [], []

    records_user_playlist = fetch_user_playlist(cursor, user)

    role_verified_list = []
    if is_artist:
        role_verified_list.append('Artist')
    if is_songwriter:
        role_verified_list.append('Songwriter')
    if is_podcaster:
        role_verified_list.append('Podcaster')
    
    role_verified = ', '.join(role_verified_list) if role_verified_list else "Pengguna Biasa"

    gender = 'Perempuan' if request.session.get('gender') == 0 else 'Laki-laki'
        
    pengguna_biasa = {
        "nama": user_info[2],
        "email": user,
        "kota_asal": user_info[7],
        "gender": gender,
        'tempat_lahir': user_info[4],
        'tanggal_lahir': user_info[5],
        "role": request.session.get('roles'),
        "playlists": playlists,
        "podcasts": podcasts,
        "albums": albums,
        "songs": songs,
        'role': 'pengguna',
        'status': 'success',
        'role_verified': role_verified,
        'status_langganan': status_langganan,
        'isArtist': is_artist,
        'isSongwriter': is_songwriter,
        'isPodcaster': is_podcaster,
        'records_user_playlist': records_user_playlist,
        'records_song_artist': records_song_artist,
        'records_song_songwriter': records_song_songwriter,
        'records_podcast': records_podcast,

    }
    return render(request, 'dashboard_pengguna.html', pengguna_biasa)

@connectdb
def dashboard_label(cursor: CursorWrapper, request):
    email = request.session.get('email')

    albums = ""

    cursor.execute("SELECT * FROM LABEL WHERE email = %s", [email])
    label = cursor.fetchone()

    if not label:
        return HttpResponseRedirect(reverse('authentication:login'))

    query =(rf"""SELECT ALBUM.judul, ALBUM.jumlah_lagu, ALBUM.total_durasi
                 FROM ALBUM
                 JOIN LABEL ON ALBUM.id_label = LABEL.id
                 WHERE LABEL.email = '{email}';
                 """)
    cursor.execute(query)
    albums = cursor.fetchall()

    context = {
        'role': 'label',
        'status': 'success',
        'id': str(label[0]),
        'nama': label[1],
        'email': label[2],
        'kontak': label[4],
        'id_pemilik_hak_cipta': str(label[5]),
        'albums': albums,
    }

    return render(request, 'dashboard_label.html', context)

def fetch_user_data(cursor: CursorWrapper, email, records_song_artist, records_song_songwriter, records_podcast):
    id_artist, id_songwriter, id_pemilik_hak_cipta_artist, id_pemilik_hak_cipta_songwriter = "", "", "", ""

    cursor.execute("SELECT * FROM ARTIST WHERE email_akun = %s", [email])
    artist = cursor.fetchone()
    if artist:
        id_artist = artist[0]
        id_pemilik_hak_cipta_artist = artist[2]
        cursor.execute("SELECT * FROM SONG WHERE id_artist = %s", [id_artist])
        artist_songs = cursor.fetchall()
        for song in artist_songs:
            id_song = song[0]
            cursor.execute("SELECT judul, durasi FROM KONTEN WHERE id = %s", [id_song])
            additional_detail_song = cursor.fetchone()
            if additional_detail_song:
                records_song_artist.append(song + additional_detail_song)

    cursor.execute("SELECT * FROM SONGWRITER WHERE email_akun = %s", [email])
    songwriter = cursor.fetchone()
    if songwriter:
        id_songwriter = songwriter[0]
        id_pemilik_hak_cipta_songwriter = songwriter[2]
        cursor.execute("SELECT id_song FROM SONGWRITER_WRITE_SONG WHERE id_songwriter = %s", [id_songwriter])
        list_id_song = cursor.fetchall()
        for song in list_id_song:
            id_song = song[0]
            cursor.execute("SELECT * FROM SONG WHERE id_konten = %s", [id_song])
            records_song_awal = cursor.fetchone()
            cursor.execute("SELECT judul, durasi FROM KONTEN WHERE id = %s", [id_song])
            additional_detail_song = cursor.fetchone()
            if records_song_awal and additional_detail_song:
                records_song_songwriter.append(records_song_awal + additional_detail_song)

    cursor.execute("SELECT * FROM PODCASTER WHERE email = %s", [email])
    podcaster = cursor.fetchone()
    if podcaster:
        cursor.execute("SELECT * FROM PODCAST WHERE email_podcaster = %s", [email])
        list_id_podcast = cursor.fetchall()
        for podcast in list_id_podcast:
            id_podcast = podcast[0]
            cursor.execute("""
                SELECT k.id, k.judul, COUNT(*) AS jumlah_episode, k.durasi 
                FROM KONTEN AS k 
                JOIN EPISODE AS e ON e.id_konten_podcast = k.id 
                WHERE k.id = %s 
                GROUP BY k.id
            """, [id_podcast])
            records_podcast.append(cursor.fetchone())

    return id_artist, id_songwriter, id_pemilik_hak_cipta_artist, id_pemilik_hak_cipta_songwriter

def fetch_user_playlist(cursor: CursorWrapper, email):
    cursor.execute("SELECT * FROM USER_PLAYLIST WHERE email_pembuat = %s", [email])
    return cursor.fetchall()

def is_premium(cursor: CursorWrapper, email):
    cursor.execute("SELECT * FROM PREMIUM WHERE email = %s", [email])
    return bool(cursor.fetchone())
#     return render(request, 'dashboard.html', context)


# def get_role_pengguna(email: str) -> list:
#     roles = []
#     with conn.cursor() as cursor:
#         cursor.execute("set search_path to marmut")
#         cursor.execute(f"SELECT * FROM ARTIST WHERE email_akun = '{email}'")
#         artist = cursor.fetchall()
#         cursor.execute(f"SELECT * FROM SONGWRITER WHERE email_akun = '{email}'")
#         songwriter = cursor.fetchall()
#         cursor.execute(f"SELECT * FROM PODCASTER WHERE email = '{email}'")
#         podcaster = cursor.fetchall()
#         cursor.execute("set search_path to public")
#     if len(artist) > 0:
#         roles.append("Artist")
#     if len(songwriter) > 0:
#         roles.append("Songwriter")
#     if len(podcaster) > 0:
#         roles.append("Podcaster")

#     return roles

# def get_songs_artist_songwriter(email: str) -> list:
#     songs = []
#     formatted_songs = []
#     with conn.cursor() as cursor:
#         cursor.execute("set search_path to marmut")
#         cursor.execute(f"SELECT id FROM ARTIST WHERE email_akun = '{email}'")
#         id_json = cursor.fetchall()
#         id_searched = str(id_json[0][0])

#         cursor.execute(f"SELECT * FROM SONG WHERE id_artist = '{id_searched}'")
#         datas = cursor.fetchall()

#         for data in datas:
#             id_konten = str(data[0])
#             cursor.execute(f"SELECT * FROM KONTEN WHERE id = '{id_konten}'")
#             tmp = cursor.fetchall()
#             songs.append(tmp)

#         for song_group in songs:
#             group_list = []
#             for song in song_group:
#                 song_dict = {
#                     'id': song[0],
#                     'title': song[1],
#                     'release_date': song[2],
#                     'year': song[3],
#                     'duration': song[4]
#                 }
#                 group_list.append(song_dict)
#             formatted_songs.append(group_list)
#         cursor.execute("set search_path to public")

#     return formatted_songs