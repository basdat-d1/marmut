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