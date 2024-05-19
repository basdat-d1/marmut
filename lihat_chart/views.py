from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render
from utils.query import connectdb
from django.urls import reverse
from django.db.backends.utils import CursorWrapper

@connectdb
def show_chart(cursor: CursorWrapper, request):
    cursor.execute("SELECT tipe FROM CHART")
    charts = cursor.fetchall()

    charts_list = []
    
    for chart in charts:
        chart_tipe = chart[0]
        if chart_tipe not in charts_list:
            charts_list.append(chart_tipe)
    
    is_podcaster = request.session.get('is_podcaster', False)
    is_artist = request.session.get('is_artist', False)
    is_songwriter = request.session.get('is_songwriter', False)
    is_podcaster = request.session.get('is_podcaster', False)
    status_langganan = request.session.get('status_langganan', 'Non-Premium')
    
    content = {
        "charts": charts_list,
        'status_langganan': status_langganan,
        'isArtist': is_artist,
        'isSongwriter': is_songwriter,
        'isPodcaster': is_podcaster,
    }
    
    return render(request, 'lihat_chart.html', content)

@connectdb
def isi_chart(cursor: CursorWrapper, request):
    playlist_type = request.GET.get('playlist_type')
    is_podcaster = request.session.get('is_podcaster', False)
    is_artist = request.session.get('is_artist', False)
    is_songwriter = request.session.get('is_songwriter', False)
    status_langganan = request.session.get('status_langganan', 'Non-Premium')
    
    query = """
    SELECT K.id, K.judul, AK.nama, K.tanggal_rilis, S.total_play
    FROM CHART AS C
    JOIN PLAYLIST AS P ON C.id_playlist = P.id
    JOIN PLAYLIST_SONG AS PS ON P.id = PS.id_playlist
    JOIN SONG AS S ON PS.id_song = S.id_konten
    JOIN KONTEN AS K ON S.id_konten = K.id
    JOIN ARTIST AS A ON S.id_artist = A.id
    JOIN AKUN AS AK ON A.email_akun = AK.email
    WHERE C.tipe = %s
    ORDER BY S.total_play DESC
    LIMIT 20
    """
    
    if playlist_type:
        cursor.execute(query, (playlist_type,))
        songs = cursor.fetchall()
        
        if songs:
            selected_playlist = {
                playlist_type: songs
            }
            
            content = {
                'playlists': selected_playlist,
                'status_langganan': status_langganan,
                'isArtist': is_artist,
                'isSongwriter': is_songwriter,
                'isPodcaster': is_podcaster,
            }
            
            return render(request, 'isi_chart.html', content)
        else:
            return HttpResponseNotFound('No songs found for this playlist.')
    else:
        return HttpResponseNotFound('Playlist type not provided.')
