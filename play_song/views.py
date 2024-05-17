import json
from django.db import connection
from django.http import JsonResponse
from django.shortcuts import render

# email_pembuat = request.user.email,
email_pembuat = 'angela93@hotmail.com'

def song_detail(request):
    judul_lagu = 'Many production choice choice'
    genres = []
    artist = ''
    songwriters = []
    daftar_playlist = []
    durasi, tanggal_rilis, tahun, total_play, total_download, album, song_id = "", "", "", "", "", "", ""

    with connection.cursor() as cursor:
        cursor.execute("Set search_path to marmut;")
        cursor.execute("""
                       SELECT genre
                       FROM genre
                       JOIN konten ON genre.id_konten = konten.id
                       WHERE konten.judul = %s;
                       """, [judul_lagu])
        result = cursor.fetchall()
        for row in result:
            genres.append(row[0])

        cursor.execute("""
                       SELECT akun.nama
                       FROM artist
                       JOIN akun ON artist.email_akun = akun.email
                       JOIN song ON artist.id = song.id_artist
                       JOIN konten ON song.id_konten = konten.id
                       WHERE konten.judul = %s;
                       """, [judul_lagu])
        result = cursor.fetchall()
        artist = result[0][0]

        cursor.execute("""
                       SELECT akun.nama
                       FROM songwriter
                          JOIN akun ON songwriter.email_akun = akun.email
                            JOIN songwriter_write_song ON songwriter.id = songwriter_write_song.id_songwriter
                            JOIN song ON songwriter_write_song.id_song = song.id_konten
                            JOIN konten ON song.id_konten = konten.id
                            WHERE konten.judul = %s;
                          """, [judul_lagu])
        result = cursor.fetchall()
        for row in result:
            songwriters.append(row[0])

        cursor.execute("""
                        SELECT 
                            konten.durasi, 
                            konten.tanggal_rilis, 
                            konten.tahun, 
                            song.total_play, 
                            song.total_download, 
                            album.judul,
                            song.id_konten
                        FROM song
                        JOIN konten ON song.id_konten = konten.id
                        JOIN album ON song.id_album = album.id
                        WHERE konten.judul = %s;
                        """, [judul_lagu])
        result = cursor.fetchall()
        durasi, tanggal_rilis, tahun, total_play, total_download, album, song_id = result[0]

        cursor.execute("""
                        SELECT user_playlist.judul, user_playlist.id_user_playlist
                        FROM user_playlist
                        JOIN akun ON akun.email = user_playlist.email_pembuat
                        WHERE akun.email = %s;
                        """, [email_pembuat])
        result = cursor.fetchall()
        for row in result:
            daftar_playlist.append({
                'judul': row[0],
                'id_playlist': row[1]
            })

    durasi_jam = durasi // 60
    durasi_menit = durasi % 60
    if durasi_jam == 0:
        durasi = str(durasi_menit) + " menit"
    else:
        durasi = str(durasi_jam) + " jam " + str(durasi_menit) + " menit"
    
    return render(request, 'song_detail.html', {
        # 'is_premium': request.user.is_authenticated and request.user.premium,
        # 'email_pembuat': request.user.email,
        'email_pembuat': email_pembuat,
        'is_premium': True,
        'song_id': song_id,
        'judul_lagu': judul_lagu,
        'genres': genres,
        'artist': artist,
        'songwriters': songwriters,
        'durasi': durasi,
        'tanggal_rilis': tanggal_rilis,
        'tahun': tahun,
        'total_play': total_play,
        'total_download': total_download,
        'album': album,
        'daftar_playlist': daftar_playlist
    })

def play(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email_pembuat = data.get('email_pembuat')
        progress = data.get('progress')
        song_id = data.get('song_id')
        
        if int(progress) > 70:
            with connection.cursor() as cursor:
                cursor.execute("Set search_path to marmut;")
                cursor.execute("""
                                UPDATE song
                                SET total_play = total_play + 1
                                WHERE id_konten = %s;
                                """, [song_id])
                
                cursor.execute("""
                                INSERT INTO akun_play_song (email_pemain, id_song, waktu)
                                VALUES (%s, %s, now());
                                """, [email_pembuat, song_id])
        
    return JsonResponse({'status': 'success'})

# from django.shortcuts import render

# def play_song(request):
#     return render(request, 'play_song.html')

# def add_song_to_user_playlist(request):
#     return render(request, 'add_song_to_user_playlist.html')