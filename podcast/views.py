from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound

# Create your views here.
def daftar_podcast(request):
    content = {
        "podcasts": [
            {
                "title": "Joe Rogan Experience",
                "durasi": "700 jam",
                "episodes": 90
            },
            {
                "title": "Bad Friends Podcast",
                "durasi": "301 jam",
                "episodes": 12
            },
            {
                "title": "Chunkz and Filly Show",
                "durasi": "100 jam",
                "episodes": 3
            },
            {
                "title": "Sidecast",
                "durasi": "420 jam",
                "episodes": 9
            }
        ]
    }

    return render(request, 'podcast.html', content)

def daftar_episode(request):
    podcast = request.GET.get('podcast')
    podcasts ={
        "Joe Rogan Experience":[
            {
                'title': 'JRE #1', 
                'description': 'with Kanye West',
                'release': "04/02/2010",
                'duration': '2 jam',
            },
            {
                'title': 'JRE #19',
                'description': 'with Ed Sheeran',
                'release': "06/01/2017",
                'duration': '3 jam',
            },
            {
                'title': 'JRE #91',
                'description': 'with theThe Weeknd',
                'release': "11/29/2019",
                'duration': '1 jam',
            },
        ],
         "Bad Friends Podcast": [
        {
            'title': 'Episode 1', 
            'description': 'Introductory Episode',
            'release': "01/15/2022",
            'duration': '1 jam',
        },
        {
            'title': 'Episode 2',
            'description': 'Guest Interview',
            'release': "01/22/2022",
            'duration': '1 jam 30 menit',
        },
        {
            'title': 'Episode 3',
            'description': 'Special Topic Discussion',
            'release': "01/29/2022",
            'duration': '2 jam',
        },
        ],
        "Chunkz and Filly Show": [
            {
                'title': 'Episode 1', 
                'description': 'Welcome to the Show',
                'release': "03/05/2023",
                'duration': '1 jam',
            },
            {
                'title': 'Episode 2',
                'description': 'Celebrity Guest Interview',
                'release': "03/12/2023",
                'duration': '1 jam',
            },
            {
                'title': 'Episode 3',
                'description': 'Interactive Audience Q&A',
                'release': "03/19/2023",
                'duration': '2 jam',
            },
        ],
         "Sidecast": [
        {
            'title': 'Sidecast #1', 
            'description': 'Introduction to Sidecast',
            'release': "07/10/2022",
            'duration': '45 menit',
        },
        {
            'title': 'Sidecast #2',
            'description': 'Special Guest Interview',
            'release': "07/17/2022",
            'duration': '1 jam',
        },
        {
            'title': 'Sidecast #3',
            'description': 'Deep Dive Discussion',
            'release': "07/24/2022",
            'duration': '1 jam',
        },
        ],
    }
    
    if podcast in podcasts:
        selected_podcast = {podcast: podcasts[podcast]}
        return render(request, 'episode.html', {'podcasts': selected_podcast})
    else:
        return HttpResponseNotFound('Podcast not found.')