# search_bar/views.py

from django.shortcuts import render

def search_view(request):
    return render(request, 'search_bar.html')
