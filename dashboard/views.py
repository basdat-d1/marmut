from django.shortcuts import render

def dashboard_pengguna_biasa(request):
    playlists = [
        {
            'judul': 'Argue get',
            'jumlah_lagu': 11,
            'total_durasi': 4596
        },
        {
            'judul': 'Health say easy',
            'jumlah_lagu': 91,
            'total_durasi': 4188
        },
    ]

    dummy_pengguna_biasa = {
        "nama": "Muhammad Hilal Darul Fauzan",
        "email": "hilalfauzan9@gmail.com",
        "kota_asal": "Jakarta",
        "gender": "Laki-laki",
        "tempat_lahir": "California",
        "tanggal_lahir": "27 April 2004",
        "role": "Pengguna Biasa",
        "playlists": playlists
    }

    return render(request, 'pengguna/dashboard_pengguna_biasa.html', dummy_pengguna_biasa)

def dashboard_premium(request):
    playlists = [
        {
            'judul': 'Radio ground everyone',
            'jumlah_lagu': 39,
            'total_durasi': 6664
        },
        {
            'judul': 'Once respond voice',
            'jumlah_lagu': 49,
            'total_durasi': 6682
        },
    ]

    dummy_premium = {
        "nama": "Robert Vang",
        "email": "donnaherring@gmail.com",
        "kota_asal": "Lake Williamfurt",
        "gender": "Laki-laki",
        "tempat_lahir": "New Bridgettown",
        "tanggal_lahir": "23 April 1998",
        "role": "Pengguna Biasa",            # Dummy premium ini sebagai pengguna biasa yang berlangganan
        "playlists": playlists
    }

    return render(request, 'pengguna/dashboard_premium.html', dummy_premium)

def dashboard_podcaster(request):
    podcasts = [
        {
            'judul': 'Record girl',
            'jumlah_episode': 5,
            'total_durasi': 167
        },
        {
            'judul': 'Their thought discover',
            'jumlah_episode': 10,
            'total_durasi': 170
        },
    ]

    dummy_podcaster = {
        "nama": "Beth White",
        "email": "hilljason@gmail.com",
        "kota_asal": "Port Bradleyburgh",
        "gender": "Laki-laki",
        "tempat_lahir": "Ryanmouth",
        "tanggal_lahir": "14 July 2000",
        "role": "Podcaster",
        "podcasts": podcasts
    }

    return render(request, 'pengguna/dashboard_podcaster.html', dummy_podcaster)

def dashboard_artist_songwriter(request):
    songs = [
        {
            'judul': 'Travel against my city',
            'total_play': 142153,
            'total_download': 10232
        },
        {
            'judul': 'Their thought discover',
            'total_play': 213243,
            'total_download': 9921
        },
    ]

    dummy_artist_songwriter = {
        "nama": "Kelly Walsh",
        "email": "barbaragreen@yahoo.com",
        "kota_asal": "Michaelstad",
        "gender": "Perempuan",
        "tempat_lahir": "Jonesbury",
        "tanggal_lahir": "21 September 1988",
        "role": "Artist/Songwriter",
        "songs": songs
    }

    return render(request, 'pengguna/dashboard_artist_songwriter.html', dummy_artist_songwriter)

def dashboard_label(request):
    albums = [
        {
            'judul': 'Enterprise-wide incremental superstructure',
            'jumlah_lagu': 85,
            'total_durasi': 421
        },
        {
            'judul': 'Reactive uniform product',
            'jumlah_lagu': 20,
            'total_durasi': 326
        },
    ]

    dummy_label = {
        "nama": "Singleton, Welch and Rios",
        "email": "derek22@hotmail.com",
        "kontak": "7185100571",
        "albums": albums
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