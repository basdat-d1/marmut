import uuid
from django.urls import reverse
from utils.query import connectdb
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.db.backends.utils import CursorWrapper

@connectdb
def user_playlist(cursor: CursorWrapper, request):
    email_pembuat = request.session.get('email')

    if request.method == 'POST':
        judul = request.POST['judul_playlist']
        deskripsi = request.POST['deskripsi_playlist']
        id_user_playlist = uuid.uuid4()
        id_playlist = uuid.uuid4()
        date_created = 'NOW()'

        cursor.execute(
                    """INSERT INTO playlist (id) VALUES (%s)
                    """, [id_playlist]
        )
        
        cursor.execute(
                    """INSERT INTO user_playlist (
                        email_pembuat, 
                        id_user_playlist, 
                        judul, 
                        deskripsi, 
                        jumlah_lagu, 
                        tanggal_dibuat, 
                        id_playlist, 
                        total_durasi
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """, [email_pembuat, id_user_playlist, judul, deskripsi, 0, date_created, id_playlist, 0]
        )
        
        return redirect('/kelolaplaylist/')
        
    cursor.execute(
                """SELECT judul, jumlah_lagu, total_durasi, id_user_playlist
                    FROM user_playlist
                    WHERE email_pembuat = %s;
                """, [email_pembuat])
    
    result = cursor.fetchall()
    playlists = []
    
    for row in result:
        playlists.append({
            'id': row[3],
            'judul': row[0],
            'jumlah_lagu': row[1],
            'total_durasi': row[2]
        })

    return render(request, 'user_playlist.html', {'playlists': playlists})

@connectdb
def ubah_playlist(cursor: CursorWrapper, request, id_playlist):
    if request.method == 'POST':
        judul = request.POST['judul_playlist']
        deskripsi = request.POST['deskripsi_playlist']

        cursor.execute(
                    """UPDATE user_playlist
                        SET judul = %s, deskripsi = %s
                        WHERE id_user_playlist = %s;
                    """, [judul, deskripsi, id_playlist])
        
        return redirect('/kelolaplaylist/')
    
    judul_playlist = ''
    deskripsi_playlist = ''

    cursor.execute(
                """SELECT judul, deskripsi
                    FROM user_playlist
                    WHERE id_user_playlist = %s;
                """, [id_playlist])
    result = cursor.fetchall()

    judul_playlist, deskripsi_playlist = result[0]

    return render(request, 'ubah_playlist.html', {
        'id': id_playlist,
        'judul': judul_playlist,
        'deskripsi': deskripsi_playlist
    })

@connectdb
def hapus_playlist(cursor: CursorWrapper, id_playlist):
    cursor.execute("""
                    DELETE FROM user_playlist
                    WHERE id_user_playlist = %s;
                    """, [id_playlist])
    
    return HttpResponseRedirect(reverse("user_playlist:user_playlist"))

@connectdb
def detail_playlist(cursor: CursorWrapper, request, id_playlist):
    cursor.execute("""
                    SELECT judul, email_pembuat, jumlah_lagu, total_durasi, tanggal_dibuat, deskripsi
                    FROM user_playlist
                    WHERE id_user_playlist = %s;
                    """, [id_playlist])
    result = cursor.fetchone()
    playlist = {
        'judul': result[0],
        'pembuat': result[1],
        'jumlah_lagu': result[2],
        'total_durasi': result[3],
        'tanggal_dibuat': result[4],
        'deskripsi': result[5]
    }

    cursor.execute("""
                    SELECT song.id_konten, song.judul, artist.nama, song.durasi
                    FROM playlist_song
                    JOIN song ON playlist_song.id_song = song.id_konten
                    JOIN artist ON song.id_artist = artist.id
                    WHERE playlist_song.id_playlist = %s;
                    """, [id_playlist])
    songs = cursor.fetchall()

    daftar_lagu = []
    for song in songs:
        daftar_lagu.append({
            'id': song[0],
            'judul': song[1],
            'artis': song[2],
            'durasi': song[3]
        })

    return render(request, 'detail_playlist.html', {
        'playlist': playlist,
        'daftar_lagu': daftar_lagu
    })

@connectdb
def tambah_lagu(cursor: CursorWrapper, request, id_playlist):
    if request.method == 'POST':
        id_lagu = request.POST['id_lagu']

        cursor.execute("""
                        SELECT COUNT(*)
                        FROM playlist_song
                        WHERE id_playlist = %s AND id_song = %s;
                        """, [id_playlist, id_lagu])
        exists = cursor.fetchone()[0]
        
        if exists == 0:
            cursor.execute("""
                           INSERT INTO playlist_song (id_playlist, id_song)
                           VALUES (%s, %s);
                           """, [id_playlist, id_lagu])

            cursor.execute("""
                           UPDATE user_playlist
                           SET jumlah_lagu = jumlah_lagu + 1, total_durasi = total_durasi + (
                               SELECT durasi FROM song WHERE id_konten = %s
                           )
                           WHERE id_user_playlist = %s;
                           """, [id_lagu, id_playlist])

            return redirect(f'/detailplaylist/{id_playlist}/')

    cursor.execute("""
                    SELECT id_konten, judul, artist.nama
                    FROM song
                    JOIN artist ON song.id_artist = artist.id;
                    """)
    songs = cursor.fetchall()

    daftar_lagu = []
    for song in songs:
        daftar_lagu.append({
            'id': song[0],
            'judul': f"{song[1]} - {song[2]}"
        })

    return render(request, 'tambah_lagu.html', {
        'id_playlist': id_playlist,
        'daftar_lagu': daftar_lagu
    })

@connectdb
def hapus_lagu(cursor: CursorWrapper, id_playlist, id_lagu):
    cursor.execute("""
                    DELETE FROM playlist_song
                    WHERE id_playlist = %s AND id_song = %s;
                    """, [id_playlist, id_lagu])

    cursor.execute("""
                   UPDATE user_playlist
                   SET jumlah_lagu = jumlah_lagu - 1, total_durasi = total_durasi - (
                       SELECT durasi FROM song WHERE id_konten = %s
                   )
                   WHERE id_user_playlist = %s;
                   """, [id_lagu, id_playlist])

    return redirect(f'/detailplaylist/{id_playlist}/')