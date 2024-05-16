from utils.query import connectdb
from django.urls import reverse
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.db.backends.utils import CursorWrapper

@connectdb
def dashboard_pengguna(cursor: CursorWrapper, request):
    email = request.session.get('email')

    cursor.execute("SELECT * FROM AKUN WHERE email = %s", [email])
    user = cursor.fetchone()

    if not user:
        return HttpResponseRedirect(reverse('authentication:login'))

    is_artist = request.session.get('is_artist', False)
    is_songwriter = request.session.get('is_songwriter', False)
    is_podcaster = request.session.get('is_podcaster', False)
    status_langganan = request.session.get('status_langganan', 'Non-Premium')

    records_song_artist, records_song_songwriter, records_podcast = [], [], []

    id_artist, id_songwriter, id_pemilik_hak_cipta_artist, id_pemilik_hak_cipta_songwriter = fetch_user_data(cursor, email, records_song_artist, records_song_songwriter, records_podcast)

    records_user_playlist = fetch_user_playlist(cursor, email)

    role_verified_list = []
    if is_artist:
        role_verified_list.append('Artist')
    if is_songwriter:
        role_verified_list.append('Songwriter')
    if is_podcaster:
        role_verified_list.append('Podcaster')
    
    role_verified = ', '.join(role_verified_list) if role_verified_list else "Pengguna Biasa"

    context = {
        'role': 'pengguna',
        'status': 'success',
        'role_verified': role_verified,
        'nama': user[2],
        'email': user[0],
        'status_langganan': status_langganan,
        'kota_asal': user[7],
        'gender': user[3],
        'tempat_lahir': user[4],
        'tanggal_lahir': user[5],
        'isArtist': is_artist,
        'isSongwriter': is_songwriter,
        'isPodcaster': is_podcaster,
        'records_user_playlist': records_user_playlist,
        'records_song_artist': records_song_artist,
        'records_song_songwriter': records_song_songwriter,
        'records_podcast': records_podcast,
    }
# from django.http import HttpResponseRedirect
# from django.urls import reverse
# from utils import query
# from utils.query import connectdb
# from django.shortcuts import redirect, render
# from django.contrib import messages
# from django.db import connection
# from django.db.backends.utils import CursorWrapper

# @connectdb
# def dashboard_pengguna(cursor: CursorWrapper, request):
#     # print("masuk dashboard_pengguna")
#     # try:
#     #     user = request.session.get['email']
#     # except:
#     #     print("email ga masuk")
#     #     return HttpResponseRedirect(reverse("authentication:login"))
#     print(request)
#     user = request.session.get["email"]
#     print(user)
    
#     playlists = ""
#     podcasts = ""
#     albums = ""
#     songs = ""
    
#     with connection.cursor() as cursor:
#         if ("Podcaster" in request.session.get['roles']):
#             query =(rf"""SELECT k.judul AS podcast_title, COUNT(e.id_episode) AS episode_count, COALESCE(SUM(e.durasi), 0) AS total_duration_minutes
#                     FROM podcast AS p
#                     JOIN konten AS k ON p.id_konten = k.id
#                     LEFT JOIN episode AS e ON p.id_konten = e.id_konten_podcast
#                     WHERE p.email_podcaster = '{user}'
#                     GROUP BY k.judul;
#                  """)
#             cursor.execute(query)
#             podcasts = cursor.fetchall()
#         elif ("Artist" in request.session.get['roles']):
#             query =(rf"""SELECT KONTEN.judul, SONG.total_play, SONG.total_download
#                     FROM KONTEN, SONG
#                     JOIN ARTIST ON SONG.id_artist = ARTIST.id
#                     WHERE ARTIST.email_akun = '{user}' AND KONTEN.id = SONG.id_konten;
#                  """)
#             cursor.execute(query)
#             songs = cursor.fetchall()
#         elif ("Songwriter" in request.session.get['roles']):
#             query =(rf"""SELECT konten.judul AS song_title, song.total_play, song.total_download
#                     FROM royalti
#                     JOIN song ON royalti.id_song = song.id_konten
#                     JOIN konten ON song.id_konten = konten.id
#                     JOIN songwriter ON royalti.id_pemilik_hak_cipta = songwriter.id_pemilik_hak_cipta
#                     WHERE songwriter.email_akun = '{user}';
#                  """)
#             cursor.execute(query)
#             songs = cursor.fetchall()

#         query =(rf"""SELECT judul, jumlah_lagu, total_durasi
#                     FROM MARMUT.user_playlist
#                     WHERE email_pembuat = '{user}';
#                  """)
#         cursor.execute(query)
#         playlists = cursor.fetchall()
        
#     pengguna_biasa = {
#         "nama": request.session.get['nama'],
#         "email": user,
#         "kota_asal": request.session.get['kota_asal'],
#         "gender": request.session.get['gender'],
#         "tempat_lahir": request.session.get['tempat_lahir'],
#         "tanggal_lahir": request.session.get['tanggal_lahir'],
#         "role": request.session.get['roles'],
#         "playlists": playlists,
#         "podcasts": podcasts,
#         "albums": albums,
#         "songs": songs
#     }
#     return render(request, 'pengguna/dashboard_pengguna.html', pengguna_biasa)
    

# def dashboard_pengguna_biasa(request):
#     # try:
#     #     # user = request.COOKIES['email']
#     # except:
#     #     return HttpResponseRedirect(reverse("authentication:login_user"))
#     user = 'dbeck@hotmail.com'
#     query_data =(rf"""SELECT judul, jumlah_lagu, total_durasi
#                     FROM MARMUT.user_playlist
#                     WHERE email_pembuat = '{user}';
#                  """)
#     data = query.run_query(query_data, None)
#     # playlists = [
#     #     {
#     #         'judul': 'Argue get',
#     #         'jumlah_lagu': 11,
#     #         'total_durasi': 4596
#     #     },
#     #     {
#     #         'judul': 'Health say easy',
#     #         'jumlah_lagu': 91,
#     #         'total_durasi': 4188
#     #     },
#     # ]

#     dummy_pengguna_biasa = {
#         "nama": "Muhammad Hilal Darul Fauzan",
#         "email": "hilalfauzan9@gmail.com",
#         "kota_asal": "Jakarta",
#         "gender": "Laki-laki",
#         "tempat_lahir": "California",
#         "tanggal_lahir": "27 April 2004",
#         "role": "Pengguna Biasa",
#         "playlists": data
#     }

#     return render(request, 'pengguna/dashboard_pengguna_biasa.html', dummy_pengguna_biasa)

# def dashboard_premium(request):
#     # try:
#     #     # user = request.COOKIES['email']
#     # except:
#     #     return HttpResponseRedirect(reverse("authentication:login_user"))
#     user = 'smithkristina@hotmail.com'
#     query_data =(rf"""SELECT judul, jumlah_lagu, total_durasi
#                     FROM MARMUT.user_playlist
#                     WHERE email_pembuat = '{user}';
#                  """)
#     data = query.run_query(query_data, None)
#     # playlists = [
#     #     {
#     #         'judul': 'Radio ground everyone',
#     #         'jumlah_lagu': 39,
#     #         'total_durasi': 6664
#     #     },
#     #     {
#     #         'judul': 'Once respond voice',
#     #         'jumlah_lagu': 49,
#     #         'total_durasi': 6682
#     #     },
#     # ]

#     dummy_premium = {
#         "nama": "Robert Vang",
#         "email": "donnaherring@gmail.com",
#         "kota_asal": "Lake Williamfurt",
#         "gender": "Laki-laki",
#         "tempat_lahir": "New Bridgettown",
#         "tanggal_lahir": "23 April 1998",
#         "role": "Pengguna Biasa",            # Dummy premium ini sebagai pengguna biasa yang berlangganan
#         "playlists": data
#     }

#     return render(request, 'pengguna/dashboard_premium.html', dummy_premium)

# def dashboard_podcaster(request):
#     # try:
#     #     # user = request.COOKIES['email']
#     # except:
#     #     return HttpResponseRedirect(reverse("authentication:login_user"))
#     user = 'myersdavid@hotmail.com'
#     query_data =(rf"""SELECT k.judul AS podcast_title, COUNT(e.id_episode) AS episode_count, COALESCE(SUM(e.durasi), 0) AS total_duration_minutes
#                     FROM MARMUT.podcast AS p
#                     JOIN MARMUT.konten AS k ON p.id_konten = k.id
#                     LEFT JOIN MARMUT.episode AS e ON p.id_konten = e.id_konten_podcast
#                     WHERE p.email_podcaster = '{user}'
#                     GROUP BY k.judul;
#                  """)
#     data = query.run_query(query_data, None)

#     dummy_podcaster = {
#         "nama": "Beth White",
#         "email": "hilljason@gmail.com",
#         "kota_asal": "Port Bradleyburgh",
#         "gender": "Laki-laki",
#         "tempat_lahir": "Ryanmouth",
#         "tanggal_lahir": "14 July 2000",
#         "role": "Podcaster",
#         "podcasts": data
#     }

#     return render(request, 'pengguna/dashboard_podcaster.html', dummy_podcaster)

# def dashboard_artist_songwriter(request):
#     # try:
#     #     # user = request.COOKIES['email']
#     # except:
#     #     return HttpResponseRedirect(reverse("authentication:login_user"))
#     user = 'robert74@gmail.com'
#     query_data =(rf"""SELECT MARMUT.KONTEN.judul, MARMUT.SONG.total_play, MARMUT.SONG.total_download
#                     FROM MARMUT.KONTEN, MARMUT.SONG
#                     JOIN MARMUT.ARTIST ON MARMUT.SONG.id_artist = MARMUT.ARTIST.id
#                     WHERE MARMUT.ARTIST.email_akun = '{user}' AND MARMUT.KONTEN.id = MARMUT.SONG.id_konten;
#                  """)
#     data = query.run_query(query_data, None)

#     dummy_artist_songwriter = {
#         "nama": "Kelly Walsh",
#         "email": "barbaragreen@yahoo.com",
#         "kota_asal": "Michaelstad",
#         "gender": "Perempuan",
#         "tempat_lahir": "Jonesbury",
#         "tanggal_lahir": "21 September 1988",
#         "role": "Artist/Songwriter",
#         "songs": data
#     }

#     return render(request, 'pengguna/dashboard_artist_songwriter.html', dummy_artist_songwriter)

# def dashboard_label(request):
#     # try:
#     #     # user = request.COOKIES['email']
#     # except:
#     #     return HttpResponseRedirect(reverse("authentication:login_user"))
#     user = 'monroejames@yahoo.com'
#     query_data =(rf"""SELECT MARMUT.ALBUM.judul, MARMUT.ALBUM.jumlah_lagu, MARMUT.ALBUM.total_durasi
#                  FROM MARMUT.ALBUM
#                  JOIN MARMUT.LABEL ON MARMUT.ALBUM.id_label = MARMUT.LABEL.id
#                  WHERE MARMUT.LABEL.email = '{user}';
#                  """)
#     data = query.run_query(query_data, None)

#     dummy_label = {
#         "nama": "Singleton, Welch and Rios",
#         "email": "derek22@hotmail.com",
#         "kontak": "7185100571",
#         "albums": data
#     }

    return render(request, 'dashboard_pengguna.html', context)

@connectdb
def dashboard_label(cursor: CursorWrapper, request):
    email = request.session.get('email')

    cursor.execute("SELECT * FROM LABEL WHERE email = %s", [email])
    label = cursor.fetchone()

    if not label:
        return HttpResponseRedirect(reverse('authentication:login'))

    id_label = label[0]
    cursor.execute("SELECT * FROM ALBUM WHERE id_label = %s", [id_label])
    records_album = cursor.fetchall()

    context = {
        'role': 'label',
        'status': 'success',
        'id': label[0],
        'nama': label[1],
        'email': label[2],
        'kontak': label[4],
        'id_pemilik_hak_cipta': label[5],
        'records_album': records_album,
    }
#     return render(request, 'label/dashboard_label.html', dummy_label)

# def dashboard(request):
#     if "email" not in request.session:
#         return redirect('authentication:login')

#     email = request.session["email"]
#     role = request.session["role"]

#     with conn.cursor() as cursor:
#         cursor.execute("set search_path to marmut")
#         cursor.execute(f"SELECT * FROM AKUN WHERE email = '{email}'")
#         user_data = cursor.fetchone()

#         if not user_data:
#             return redirect('authentication:login')
        
#         cursor.execute(f"SELECT * FROM PREMIUM WHERE email = '{email}'")
#         premium = cursor.fetchone()
#         if premium:
#             is_premium = True
#         else:
#             is_premium = False
        
#         cursor.execute("set search_path to public")

#     roles = get_role_pengguna(email)
#     context = {
#         'is_logged_in': True,
#         'user': user_data,
#         'role': role,
#         'roles': roles,
#         'is_premium': is_premium
#     }
#     if ("Artist" in roles and "Songwriter" in roles):
#         context['songs'] = get_songs_artist_songwriter(email)

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