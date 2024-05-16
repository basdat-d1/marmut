# auth/views.py
import uuid
import random
import datetime
import re
from django.urls import reverse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.db.backends.utils import CursorWrapper
from django.http import HttpResponseRedirect
from utils.query import connectdb

def authentication(request):
    return render(request, 'authentication.html')

def register(request):
    return render(request, 'register.html')

@connectdb
def register_pengguna(cursor: CursorWrapper, request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        nama = request.POST.get('nama')
        gender = request.POST.get('gender')
        tempat_lahir = request.POST.get('tempat_lahir')
        tanggal_lahir = request.POST.get('tanggal_lahir')
        kota_asal = request.POST.get('kota_asal')
        roles = request.POST.getlist('role')

        # Validasi email
        regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        if not re.fullmatch(regex, email):
            messages.error(request, "Email tidak valid")
            return render(request, 'registration_form/register_pengguna.html', {'form': request.POST})

        # Cek kelengkapan data
        if not email or not password or not nama or not gender or not tempat_lahir or not tanggal_lahir or not kota_asal:
            messages.error(request, "Data yang diisikan belum lengkap")
            return render(request, 'registration_form/register_pengguna.html', {'form': request.POST})

        # Cek apakah email sudah ada di tabel AKUN atau LABEL
        cursor.execute("SELECT * FROM AKUN WHERE email = %s", [email])
        user = cursor.fetchone()
        cursor.execute("SELECT * FROM LABEL WHERE email = %s", [email])
        label = cursor.fetchone()

        # Jika email sudah ada
        if user or label:
            messages.error(request, "Email sudah pernah didaftarkan.")
            return render(request, 'registration_form/register_pengguna.html', {'form': request.POST})

        # Cek panjang password minimal 8 karakter
        if len(password) < 8:
            messages.error(request, "Password minimal harus 8 karakter.")
            return render(request, 'registration_form/register_pengguna.html', {'form': request.POST})
        
        gender_info = 0 if gender == 'Perempuan' else 1
        is_verified = bool(roles)

        # Insert data ke tabel AKUN
        cursor.execute(
            """INSERT INTO AKUN(email, password, nama, gender, tempat_lahir, tanggal_lahir, is_verified, kota_asal) VALUES 
                (%s, %s, %s, %s, %s, %s, %s, %s)""", 
                (email, password, nama, gender_info, tempat_lahir, tanggal_lahir, is_verified, kota_asal)
        )
    
        # Insert data ke tabel role yang sesuai
        for role in roles:
            if role == "Podcaster":
                cursor.execute("INSERT INTO PODCASTER(email) VALUES (%s)", [email])
            elif role == "Artist":
                id_artist = str(uuid.uuid4())
                cursor.execute('SELECT id FROM PEMILIK_HAK_CIPTA')
                ids = cursor.fetchall()
                id_pemilik_hak_cipta = str(random.choice(ids)[0])
                cursor.execute("INSERT INTO ARTIST(id, email_akun, id_pemilik_hak_cipta) VALUES (%s, %s, %s)",
                                (id_artist, email, id_pemilik_hak_cipta))
            elif role == "Songwriter":
                id_songwriter = str(uuid.uuid4())
                cursor.execute('SELECT id FROM PEMILIK_HAK_CIPTA')
                ids = cursor.fetchall()
                id_pemilik_hak_cipta = str(random.choice(ids)[0])
                cursor.execute("INSERT INTO SONGWRITER(id, email_akun, id_pemilik_hak_cipta) VALUES (%s, %s, %s)",
                                (id_songwriter, email, id_pemilik_hak_cipta))
        
        messages.success(request, 'Akun Anda telah berhasil dibuat!')
        return redirect('authentication:login')

    return render(request, 'registration_form/register_pengguna.html')

@connectdb
def register_label(cursor: CursorWrapper, request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        nama = request.POST.get('nama')
        kontak = request.POST.get('kontak')
        id_label = str(uuid.uuid4())

        # Validasi email
        regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        if not re.fullmatch(regex, email):
            messages.error(request, "Email tidak valid")
            return render(request, 'registration_form/register_label.html', {'form': request.POST})

        # Cek kelengkapan data
        if not email or not password or not nama or not kontak:
            messages.error(request, "Data yang diisikan belum lengkap")
            return render(request, 'registration_form/register_label.html', {'form': request.POST})

        # Cek apakah email sudah ada di tabel AKUN atau LABEL
        cursor.execute("SELECT * FROM AKUN WHERE email = %s", [email])
        user = cursor.fetchone()
        cursor.execute("SELECT * FROM LABEL WHERE email = %s", [email])
        label = cursor.fetchone()

        # Jika email sudah ada
        if user or label:
            messages.error(request, "Email sudah pernah didaftarkan.")
            return render(request, 'registration_form/register_label.html', {'form': request.POST})
        
        # Cek panjang password minimal 8 karakter
        if len(password) < 8:
            messages.error(request, "Password minimal harus 8 karakter.")
            return render(request, 'registration_form/register_label.html', {'form': request.POST})

        # Insert data ke tabel LABEL
        cursor.execute('SELECT id FROM PEMILIK_HAK_CIPTA')
        ids = cursor.fetchall()
        id_pemilik_hak_cipta = str(random.choice(ids)[0])

        cursor.execute(
            """INSERT INTO LABEL(id, nama, email, password, kontak, id_pemilik_hak_cipta) VALUES 
                (%s, %s, %s, %s, %s, %s)""", 
                (id_label, nama, email, password, kontak, id_pemilik_hak_cipta)
        )
        
        messages.success(request, 'Akun Anda telah berhasil dibuat!')
        return redirect('authentication:login')
        
    return render(request, 'registration_form/register_label.html')

@connectdb
def login(cursor: CursorWrapper, request):
    context = {}

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        cursor.execute("SELECT * FROM AKUN WHERE email = %s", [email])
        user = cursor.fetchone()

        cursor.execute("SELECT * FROM LABEL WHERE email = %s", [email])
        label = cursor.fetchone()

        # Kalo email atau password salah
        if not user and not label:
            context["message"] = "Email atau password salah"
            return render(request, "login.html", context)

        # Jika password benar
        if user and user[1] == password:
            return handle_pengguna_login(cursor, request, user)
        elif label and label[3] == password:
            return handle_label_login(cursor, request, label)

    return render(request, 'login.html', context)

def handle_pengguna_login(cursor: CursorWrapper, request, user):
    email = user[0]
    is_artist, is_songwriter, is_podcaster = False, False, False
    status_langganan = "Non-Premium"

    records_song_artist, records_song_songwriter, records_podcast = [], [], []

    # Fetch data pengguna
    id_artist, id_songwriter, id_pemilik_hak_cipta_artist, id_pemilik_hak_cipta_songwriter = fetch_user_data(cursor, email, records_song_artist, records_song_songwriter, records_podcast)

    # Cek apakah user artist
    cursor.execute("SELECT * FROM ARTIST WHERE email_akun = %s", [email])
    artist = cursor.fetchone()
    if artist:
        is_artist = True
    # Cek apakah user songwriter
    cursor.execute("SELECT * FROM SONGWRITER WHERE email_akun = %s", [email])
    songwriter = cursor.fetchone()
    if songwriter:
        is_songwriter = True
    # Cek apakah user artist
    cursor.execute("SELECT * FROM PODCASTER WHERE email = %s", [email])
    podcaster = cursor.fetchone()
    if podcaster:
        is_podcaster = True
    # Cek apakah user premium
    if is_premium(cursor, email):
        status_langganan = "Premium"

    request.session["email"] = email
    request.session["role"] = 'pengguna'
    request.session["status_langganan"] = status_langganan
    request.session["is_artist"] = is_artist
    request.session["is_songwriter"] = is_songwriter
    request.session["is_podcaster"] = is_podcaster
    request.session["id_artist"] = str(id_artist)
    request.session["id_songwriter"] = str(id_songwriter)
    request.session["id_pemilik_hak_cipta_artist"] = str(id_pemilik_hak_cipta_artist)
    request.session["id_pemilik_hak_cipta_songwriter"] = str(id_pemilik_hak_cipta_songwriter)
    request.session['last_login'] = str(datetime.datetime.now())

    return HttpResponseRedirect(reverse('dashboard:dashboard_pengguna'))

def handle_label_login(cursor: CursorWrapper, request, label):
    email = label[2]
    id_label = label[0]
    cursor.execute("SELECT * FROM ALBUM WHERE id_label = %s", [str(id_label)])
    albums = cursor.fetchall()

    request.session["email"] = email
    request.session["role"] = 'label'
    request.session["id_label"] = str(id_label)
    request.session["id_pemilik_hak_cipta_label"] = str(label[5])

    return HttpResponseRedirect(reverse('dashboard:dashboard_label'))

def fetch_user_data(cursor: CursorWrapper, email, records_song_artist, records_song_songwriter, records_podcast):
    id_artist, id_songwriter, id_pemilik_hak_cipta_artist, id_pemilik_hak_cipta_songwriter = "", "", "", ""

    # Fetch data artist
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

    # Fetch data songwriter
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

    # Fetch data podcaster
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

def logout(request):
    request.session.flush()
    return HttpResponseRedirect(reverse('authentication:authentication'))