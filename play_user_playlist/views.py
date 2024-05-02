from django.shortcuts import render

def play_user_playlist(request):
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

    return render(request, 'play_user_playlist.html', context)