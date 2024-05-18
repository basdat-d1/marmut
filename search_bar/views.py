import uuid
from django.shortcuts import render
from django.db.backends.utils import CursorWrapper
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.http import HttpResponseRedirect

from utils.query import connectdb

@connectdb
@csrf_exempt
def search_view(cursor: CursorWrapper, request):
    if request.method == 'GET':
        query = request.GET.get('query', '')

        # Initialize an empty list to store search results
        search_results = []

        # Search for songs, podcasts, user playlists, and labels
        cursor.execute("""
            SELECT k.judul AS judul, 'Song' AS tipe, a.email_akun AS oleh, k.id
            FROM KONTEN k
            JOIN SONG s ON k.id = s.id_konten
            JOIN ARTIST a ON s.id_artist = a.id
            WHERE k.judul ILIKE %s

            UNION ALL

            SELECT k.judul AS judul, 'Podcast' AS tipe, p.email AS oleh, k.id
            FROM KONTEN k
            JOIN PODCAST pc ON k.id = pc.id_konten
            JOIN PODCASTER p ON pc.email_podcaster = p.email
            WHERE k.judul ILIKE %s

            UNION ALL

            SELECT up.judul AS judul, 'User Playlist' AS tipe, ak.email AS oleh, up.id_user_playlist
            FROM USER_PLAYLIST up
            JOIN AKUN ak ON up.email_pembuat = ak.email
            WHERE up.judul ILIKE %s

            UNION ALL

            SELECT l.nama AS judul, 'Label' AS tipe, l.email AS oleh, l.id
            FROM LABEL l
            WHERE l.nama ILIKE %s
        """, ['%' + query + '%', '%' + query + '%', '%' + query + '%', '%' + query + '%'])

        # Fetch all the results
        search_results = cursor.fetchall()

        # Debugging: Print query and search results
        print("Query:", query)
        print("Search results:", search_results)

        # Render the search results template with the search query and results
        return render(request, 'search_bar.html', {'query': query, 'search_results': search_results})
    else:
        # Jika metode yang digunakan bukan GET
        return render(request, 'error.html', {'message': 'Metode yang digunakan tidak valid'})

@connectdb
@csrf_exempt
def detail_item_view(cursor: CursorWrapper, request, item_id):
    try:
        # Ensure item_id is a string
        item_id_str = str(item_id)
        # Convert item_id to a UUID
        item_uuid = uuid.UUID(item_id_str)
    except ValueError as e:
        # Print the error and item_id for debugging
        print("Error converting item_id to UUID:", e)
        print("item_id:", item_id)
        print("item_id type:", type(item_id))
        return render(request, 'error.html', {'message': 'ID tidak valid'})

    cursor.execute("""
        SELECT k.judul, k.tanggal_rilis, k.tahun, k.durasi, 
               a.email_akun AS oleh
        FROM KONTEN k
        JOIN SONG s ON k.id = s.id_konten
        JOIN ARTIST a ON s.id_artist = a.id
        WHERE k.id = %s

        UNION ALL

        SELECT k.judul, k.tanggal_rilis, k.tahun, k.durasi, 
               p.email AS oleh
        FROM KONTEN k
        JOIN PODCAST pc ON k.id = pc.id_konten
        JOIN PODCASTER p ON pc.email_podcaster = p.email
        WHERE k.id = %s

        UNION ALL

        SELECT up.judul, up.tanggal_dibuat, NULL, up.total_durasi, 
               ak.email AS oleh
        FROM USER_PLAYLIST up
        JOIN AKUN ak ON up.email_pembuat = ak.email
        WHERE up.id_user_playlist = %s
    """, [str(item_uuid), str(item_uuid), str(item_uuid)])

    item_data = cursor.fetchone()

    if item_data:
        item_type = 'Song' if item_data[2] else 'Podcast' if item_data[1] else 'User Playlist'
        item_title, tanggal_rilis, tahun, durasi, oleh = item_data
        return render(request, 'detail_item.html', {'item_type': item_type, 'item_title': item_title,
                                                     'tanggal_rilis': tanggal_rilis, 'tahun': tahun,
                                                     'durasi': durasi, 'oleh': oleh})
    else:
        return render(request, 'error.html', {'message': 'Item tidak ditemukan'})