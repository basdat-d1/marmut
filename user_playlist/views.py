from django.shortcuts import render

def user_playlist(request):
    playlists = [
        {
            'judul': 'Radio ground everyone',
            'jumlah_lagu': 39,
            'total_durasi': 6664
        },
        {
            'judul': 'Health say easy',
            'jumlah_lagu': 91,
            'total_durasi': 4188
        },
        {
            'judul': 'Rich people',
            'jumlah_lagu': 49,
            'total_durasi': 6682
        },
    ]

    context = {
        "playlists": playlists
    }

    return render(request, 'user_playlist.html', context)

def tambah_playlist(request):
    return render(request, 'tambah_playlist.html')

def ubah_playlist(request):
    return render(request, 'ubah_playlist.html')

def detail_playlist(request):
    songs = [
        {
            'judul': 'Travel against my city',
            'email_pembuat': 'smithkristina@hotmail.com',
            'durasi': 3
        },
        {
            'judul': 'Their thought discover',
            'email_pembuat': 'hilalfauzan9@gmail.com',
            'durasi': 4
        },
    ]

    context = {
        "songs": songs
    }

    return render(request, 'detail_playlist.html', context)

def tambah_lagu(request):
    songs_artists = [
        ("Pretty mother reduce table", "Lauren Harrison"),
        ("Available long suggest least", "John Brooks"),
        ("For young sound concern", "Paul Scott"),
        ("Travel against my city", "Tanya Ford"),
        ("Trial PM", "Cristian Jackson"),
        ("Country lay shake sort", "Cynthia Jordan"),
        ("Cause yourself", "Kimberly Rodriguez"),
        ("Cost might five air", "Kaitlyn Curry"),
        ("Radio front number", "Cristian Jackson"),
        ("Open population", "Lauren Harrison"),
        ("Over trade four", "Adam Howell"),
        ("Raise right institution", "Kimberly Rodriguez"),
        ("Oil water organization service", "Paul Scott"),
        ("Activity report consumer business", "Kaitlyn Curry"),
        ("Ball or task early would", "Paul Scott"),
        ("Mouth under local", "Cristian Jackson"),
        ("Decision how pattern money forget", "Jessica Meyer"),
        ("History film east though until", "Kaitlyn Curry"),
        ("College offer expert", "Kimberly Rodriguez"),
        ("Others own serious affect", "Cristian Jackson"),
        ("Near source cup member", "Jessica Meyer"),
        ("Foot north", "Kaitlyn Curry"),
        ("Various Republican process method", "Cristian Jackson"),
        ("Race we TV difference", "Cynthia Jordan"),
        ("Reduce raise garden", "Cristian Jackson"),
        ("Walk campaign company agent day", "John Brooks"),
        ("Many speech feel wish", "Cristian Jackson"),
        ("Bring performance sound why", "Jessica Meyer"),
        ("Enough campaign drive", "John Brooks"),
        ("Prepare choice address none", "Tanya Ford"),
        ("Board majority attorney", "John Brooks"),
        ("Site general indicate this", "Cristian Jackson"),
        ("Less teach everyone war training", "Paul Scott"),
        ("Me magazine organization result", "Lauren Harrison"),
        ("Kind thing will head", "Adam Howell"),
        ("Keep according short beat", "Cristian Jackson"),
        ("Guess conference detail", "Jessica Meyer"),
        ("Positive she", "Cristian Jackson"),
        ("Remain good suddenly party", "Kimberly Rodriguez"),
        ("Discover but million nice up", "Tanya Ford"),
        ("Tonight dream these another", "Cristian Jackson"),
        ("Begin could western customer", "Paul Scott"),
        ("Single know that you", "Adam Howell"),
        ("Simple stand still lay", "Cristian Jackson"),
        ("Table half level actually", "Paul Scott"),
        ("Your quickly result military board", "Paul Scott"),
        ("Financial many evidence lawyer", "Kaitlyn Curry"),
        ("Generation her eat quite share", "Tanya Ford"),
        ("Trade tax", "Tanya Ford"),
        ("Game hard agent", "Adam Howell")
    ]

    all_songs = [{'id': str(i+1), 'title': title, 'artist': artist} for i, (title, artist) in enumerate(songs_artists)]
    
    context = {
        'all_songs': all_songs
    }

    return render(request, 'tambah_lagu.html', context)