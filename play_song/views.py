from django.shortcuts import render

def play_song(request):
    return render(request, 'play_song.html')

def add_song_to_user_playlist(request):
    return render(request, 'add_song_to_user_playlist.html')