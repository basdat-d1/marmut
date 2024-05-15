from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from utils import query

def dashboard_pengguna_biasa(request):
    # try:
    #     # user = request.COOKIES['email']
    # except:
    #     return HttpResponseRedirect(reverse("authentication:login_user"))
    user = 'dbeck@hotmail.com'
    query_data =(rf"""SELECT judul, jumlah_lagu, total_durasi
                    FROM MARMUT.user_playlist
                    WHERE email_pembuat = '{user}';
                 """)
    data = query.run_query(query_data, None)
    # playlists = [
    #     {
    #         'judul': 'Argue get',
    #         'jumlah_lagu': 11,
    #         'total_durasi': 4596
    #     },
    #     {
    #         'judul': 'Health say easy',
    #         'jumlah_lagu': 91,
    #         'total_durasi': 4188
    #     },
    # ]

    dummy_pengguna_biasa = {
        "nama": "Muhammad Hilal Darul Fauzan",
        "email": "hilalfauzan9@gmail.com",
        "kota_asal": "Jakarta",
        "gender": "Laki-laki",
        "tempat_lahir": "California",
        "tanggal_lahir": "27 April 2004",
        "role": "Pengguna Biasa",
        "playlists": data
    }

    return render(request, 'pengguna/dashboard_pengguna_biasa.html', dummy_pengguna_biasa)

def dashboard_premium(request):
    # try:
    #     # user = request.COOKIES['email']
    # except:
    #     return HttpResponseRedirect(reverse("authentication:login_user"))
    user = 'smithkristina@hotmail.com'
    query_data =(rf"""SELECT judul, jumlah_lagu, total_durasi
                    FROM MARMUT.user_playlist
                    WHERE email_pembuat = '{user}';
                 """)
    data = query.run_query(query_data, None)
    # playlists = [
    #     {
    #         'judul': 'Radio ground everyone',
    #         'jumlah_lagu': 39,
    #         'total_durasi': 6664
    #     },
    #     {
    #         'judul': 'Once respond voice',
    #         'jumlah_lagu': 49,
    #         'total_durasi': 6682
    #     },
    # ]

    dummy_premium = {
        "nama": "Robert Vang",
        "email": "donnaherring@gmail.com",
        "kota_asal": "Lake Williamfurt",
        "gender": "Laki-laki",
        "tempat_lahir": "New Bridgettown",
        "tanggal_lahir": "23 April 1998",
        "role": "Pengguna Biasa",            # Dummy premium ini sebagai pengguna biasa yang berlangganan
        "playlists": data
    }

    return render(request, 'pengguna/dashboard_premium.html', dummy_premium)

def dashboard_podcaster(request):
    # try:
    #     # user = request.COOKIES['email']
    # except:
    #     return HttpResponseRedirect(reverse("authentication:login_user"))
    user = 'myersdavid@hotmail.com'
    query_data =(rf"""SELECT k.judul AS podcast_title, COUNT(e.id_episode) AS episode_count, COALESCE(SUM(e.durasi), 0) AS total_duration_minutes
                    FROM MARMUT.podcast AS p
                    JOIN MARMUT.konten AS k ON p.id_konten = k.id
                    LEFT JOIN MARMUT.episode AS e ON p.id_konten = e.id_konten_podcast
                    WHERE p.email_podcaster = '{user}'
                    GROUP BY k.judul;
                 """)
    data = query.run_query(query_data, None)

    dummy_podcaster = {
        "nama": "Beth White",
        "email": "hilljason@gmail.com",
        "kota_asal": "Port Bradleyburgh",
        "gender": "Laki-laki",
        "tempat_lahir": "Ryanmouth",
        "tanggal_lahir": "14 July 2000",
        "role": "Podcaster",
        "podcasts": data
    }

    return render(request, 'pengguna/dashboard_podcaster.html', dummy_podcaster)

def dashboard_artist_songwriter(request):
    # try:
    #     # user = request.COOKIES['email']
    # except:
    #     return HttpResponseRedirect(reverse("authentication:login_user"))
    user = 'robert74@gmail.com'
    query_data =(rf"""SELECT MARMUT.KONTEN.judul, MARMUT.SONG.total_play, MARMUT.SONG.total_download
                    FROM MARMUT.KONTEN, MARMUT.SONG
                    JOIN MARMUT.ARTIST ON MARMUT.SONG.id_artist = MARMUT.ARTIST.id
                    WHERE MARMUT.ARTIST.email_akun = '{user}' AND MARMUT.KONTEN.id = MARMUT.SONG.id_konten;
                 """)
    data = query.run_query(query_data, None)

    dummy_artist_songwriter = {
        "nama": "Kelly Walsh",
        "email": "barbaragreen@yahoo.com",
        "kota_asal": "Michaelstad",
        "gender": "Perempuan",
        "tempat_lahir": "Jonesbury",
        "tanggal_lahir": "21 September 1988",
        "role": "Artist/Songwriter",
        "songs": data
    }

    return render(request, 'pengguna/dashboard_artist_songwriter.html', dummy_artist_songwriter)

def dashboard_label(request):
    # try:
    #     # user = request.COOKIES['email']
    # except:
    #     return HttpResponseRedirect(reverse("authentication:login_user"))
    user = 'monroejames@yahoo.com'
    query_data =(rf"""SELECT MARMUT.ALBUM.judul, MARMUT.ALBUM.jumlah_lagu, MARMUT.ALBUM.total_durasi
                 FROM MARMUT.ALBUM
                 JOIN MARMUT.LABEL ON MARMUT.ALBUM.id_label = MARMUT.LABEL.id
                 WHERE MARMUT.LABEL.email = '{user}';
                 """)
    data = query.run_query(query_data, None)

    dummy_label = {
        "nama": "Singleton, Welch and Rios",
        "email": "derek22@hotmail.com",
        "kontak": "7185100571",
        "albums": data
    }

    return render(request, 'label/dashboard_label.html', dummy_label)

def dashboard(request):
    if "email" not in request.session:
        return redirect('authentication:login')

    email = request.session["email"]
    role = request.session["role"]

    with conn.cursor() as cursor:
        cursor.execute("set search_path to marmut")
        cursor.execute(f"SELECT * FROM AKUN WHERE email = '{email}'")
        user_data = cursor.fetchone()

        if not user_data:
            return redirect('authentication:login')
        
        cursor.execute(f"SELECT * FROM PREMIUM WHERE email = '{email}'")
        premium = cursor.fetchone()
        if premium:
            is_premium = True
        else:
            is_premium = False
        
        cursor.execute("set search_path to public")

    roles = get_role_pengguna(email)
    context = {
        'is_logged_in': True,
        'user': user_data,
        'role': role,
        'roles': roles,
        'is_premium': is_premium
    }
    if ("Artist" in roles and "Songwriter" in roles):
        context['songs'] = get_songs_artist_songwriter(email)

    return render(request, 'dashboard.html', context)


def get_role_pengguna(email: str) -> list:
    roles = []
    with conn.cursor() as cursor:
        cursor.execute("set search_path to marmut")
        cursor.execute(f"SELECT * FROM ARTIST WHERE email_akun = '{email}'")
        artist = cursor.fetchall()
        cursor.execute(f"SELECT * FROM SONGWRITER WHERE email_akun = '{email}'")
        songwriter = cursor.fetchall()
        cursor.execute(f"SELECT * FROM PODCASTER WHERE email = '{email}'")
        podcaster = cursor.fetchall()
        cursor.execute("set search_path to public")
    if len(artist) > 0:
        roles.append("Artist")
    if len(songwriter) > 0:
        roles.append("Songwriter")
    if len(podcaster) > 0:
        roles.append("Podcaster")

    return roles

def get_songs_artist_songwriter(email: str) -> list:
    songs = []
    formatted_songs = []
    with conn.cursor() as cursor:
        cursor.execute("set search_path to marmut")
        cursor.execute(f"SELECT id FROM ARTIST WHERE email_akun = '{email}'")
        id_json = cursor.fetchall()
        id_searched = str(id_json[0][0])

        cursor.execute(f"SELECT * FROM SONG WHERE id_artist = '{id_searched}'")
        datas = cursor.fetchall()

        for data in datas:
            id_konten = str(data[0])
            cursor.execute(f"SELECT * FROM KONTEN WHERE id = '{id_konten}'")
            tmp = cursor.fetchall()
            songs.append(tmp)

        for song_group in songs:
            group_list = []
            for song in song_group:
                song_dict = {
                    'id': song[0],
                    'title': song[1],
                    'release_date': song[2],
                    'year': song[3],
                    'duration': song[4]
                }
                group_list.append(song_dict)
            formatted_songs.append(group_list)
        cursor.execute("set search_path to public")

    return formatted_songs