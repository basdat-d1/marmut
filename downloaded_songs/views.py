from django.shortcuts import render

def downloaded_songs(request):
    return render(request, 'downloaded_songs.html')

