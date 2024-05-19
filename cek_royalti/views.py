from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import redirect, render
from django.db.backends.utils import CursorWrapper
from django.http import HttpResponseRedirect
from utils.query import connectdb

@connectdb
def cek_royalti(cursor: CursorWrapper, request):
    try:
        email = request.session.get('email')
    except:
        return HttpResponseRedirect(reverse("authentication:login_user"))
    
    royalties = []

    if request.session.get('is_artist'):
        query =(rf"""SELECT k.judul AS song_judul, a.judul AS album_judul, s.total_play, s.total_download, CONCAT('Rp ', (phc.rate_royalti::BIGINT * s.total_play::BIGINT)) AS total_royalti
                    FROM song s
                    JOIN album a ON s.id_album = a.id
                    JOIN royalti r ON s.id_konten = r.id_song
                    JOIN pemilik_hak_cipta phc ON r.id_pemilik_hak_cipta = phc.id
                    JOIN konten k ON s.id_konten = k.id
                    WHERE phc.id in (SELECT id_pemilik_hak_cipta FROM artist WHERE email_akun = '{email}')
                    ORDER BY album_judul;
                                    """)
        cursor.execute(query)
        royalties_artist = cursor.fetchall()
        for royalti in royalties_artist:
            royalties.append(royalti)
    elif request.session.get('is_songwriter'):
        query =(rf"""SELECT k.judul AS song_judul, a.judul AS album_judul, s.total_play, s.total_download, CONCAT('Rp ', (phc.rate_royalti::BIGINT * s.total_play::BIGINT)) AS total_royalti
                    FROM song s
                    JOIN album a ON s.id_album = a.id
                    JOIN royalti r ON s.id_konten = r.id_song
                    JOIN pemilik_hak_cipta phc ON r.id_pemilik_hak_cipta = phc.id
                    JOIN konten k ON s.id_konten = k.id
                    WHERE phc.id in (SELECT id_pemilik_hak_cipta FROM songwriter WHERE email_akun = '{email}')
                    ORDER BY album_judul;
                                    """)
        cursor.execute(query)
        royalties_songwriter = cursor.fetchall()
        for royalti in royalties_songwriter:
            royalties.append(royalti)
    
    context = {
        "royalties": royalties,
        'status_langganan': request.session.get('status_langganan'),
        'isArtist': request.session.get('is_artist'),
        'isSongwriter': request.session.get('is_songwriter'),
        'isPodcaster': request.session.get('is_podcaster'),
    }

    return render(request, 'cek_royalti.html', context)


@connectdb
def cek_royalti_label(cursor: CursorWrapper, request):
    try:
        email = request.session.get('email')
    except:
        return HttpResponseRedirect(reverse("authentication:login_user"))
    
    royalties = []

    query =(rf"""SELECT k.judul AS song_judul, a.judul AS album_judul, s.total_play, s.total_download, CONCAT('Rp ', (phc.rate_royalti::BIGINT * s.total_play::BIGINT)) AS total_royalti
                FROM song s
                JOIN album a ON s.id_album = a.id
                JOIN royalti r ON s.id_konten = r.id_song
                JOIN pemilik_hak_cipta phc ON r.id_pemilik_hak_cipta = phc.id
                JOIN konten k ON s.id_konten = k.id
                WHERE phc.id in (SELECT id_pemilik_hak_cipta FROM label WHERE email = '{email}')
                ORDER BY album_judul;
                                """)
    cursor.execute(query)
    royalties= cursor.fetchall()
    
    context = {
        "royalties": royalties,
        'status_langganan': request.session.get('status_langganan'),
        'isArtist': request.session.get('is_artist'),
        'isSongwriter': request.session.get('is_songwriter'),
        'isPodcaster': request.session.get('is_podcaster'),
    }

    return render(request, 'cek_royalti.html', context)

