from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound

# Create your views here.
def show_chart(request):
    content = {
        "chart": [
            {
                'title': 'Daily Top 20', 
            },
            {
                'title': 'Weekly Top 20'
            },
            {
                'title': 'Monthly Top 20'
            },
            {
                'title': 'Yearly Top 20'
            }
        ]
    }

    return render(request, 'lihat_chart.html', content)

def isi_chart(request):
    playlist_type = request.GET.get('playlist_type')
    playlists = {
        "Daily Top 20": [
            {
                'title_song': 'All of the Lights', 
                'artist': 'Kanye West',
                'release': "04/02/2010",
                'total_plays': '1010200303',
            },
            {
                'title_song': 'Shape of You',
                'artist': 'Ed Sheeran',
                'release': "06/01/2017",
                'total_plays': '1809058562',
            },
            {
                'title_song': 'Blinding Lights',
                'artist': 'The Weeknd',
                'release': "11/29/2019",
                'total_plays': '1866019781',
            },
            {
                'title_song': 'Someone Like You',
                'artist': 'Adele',
                'release': "01/24/2011",
                'total_plays': '1438525718',
            },
            {
                'title_song': 'Uptown Funk',
                'artist': 'Mark Ronson ft. Bruno Mars',
                'release': "11/10/2014",
                'total_plays': '1717439761',
            },
        ],
        "Weekly Top 20": [
            {
                'title_song': 'Dance Monkey', 
                'artist': 'Tones and I',
                'release': "05/10/2019",
                'total_plays': '1432624200',
            },
            {
                'title_song': 'Rockstar',
                'artist': 'DaBaby ft. Roddy Ricch',
                'release': "04/17/2020",
                'total_plays': '1126439545',
            },
            {
                'title_song': 'Levitating',
                'artist': 'Dua Lipa ft. DaBaby',
                'release': "03/27/2020",
                'total_plays': '1040922402',
            },
            {
                'title_song': 'Watermelon Sugar',
                'artist': 'Harry Styles',
                'release': "05/15/2020",
                'total_plays': '1039243680',
            },
            {
                'title_song': 'Bad Guy',
                'artist': 'Billie Eilish',
                'release': "03/29/2019",
                'total_plays': '1032976847',
            },
        ],
        "Monthly Top 20": [
            {
                'title_song': 'Old Town Road', 
                'artist': 'Lil Nas X ft. Billy Ray Cyrus',
                'release': "12/03/2018",
                'total_plays': '1333789236',
            },
            {
                'title_song': 'Shape of You',
                'artist': 'Ed Sheeran',
                'release': "06/01/2017",
                'total_plays': '1216113561',
            },
            {
                'title_song': 'Dance Monkey',
                'artist': 'Tones and I',
                'release': "05/10/2019",
                'total_plays': '1164877778',
            },
            {
                'title_song': 'Someone Like You',
                'artist': 'Adele',
                'release': "01/24/2011",
                'total_plays': '1144143147',
            },
            {
                'title_song': 'Closer',
                'artist': 'The Chainsmokers ft. Halsey',
                'release': "07/29/2016",
                'total_plays': '1125363427',
            },
        ],
        "Yearly Top 20": [
            {
                'title_song': 'Despacito', 
                'artist': 'Luis Fonsi ft. Daddy Yankee',
                'release': "01/12/2017",
                'total_plays': '7835415876',
            },
            {
                'title_song': 'Shape of You',
                'artist': 'Ed Sheeran',
                'release': "06/01/2017",
                'total_plays': '4575480214',
            },
            {
                'title_song': 'Uptown Funk',
                'artist': 'Mark Ronson ft. Bruno Mars',
                'release': "11/10/2014",
                'total_plays': '3699758194',
            },
            {
                'title_song': 'Thinking Out Loud',
                'artist': 'Ed Sheeran',
                'release': "09/24/2014",
                'total_plays': '3316963642',
            },
            {
                'title_song': 'Closer',
                'artist': 'The Chainsmokers ft. Halsey',
                'release': "07/29/2016",
                'total_plays': '3047880233',
            },
        ],
    }

    if playlist_type in playlists:
        selected_playlist = {playlist_type: playlists[playlist_type]}
        return render(request, 'isi_chart.html', {'playlists': selected_playlist})
    else:
        return HttpResponseNotFound('Playlist not found.')