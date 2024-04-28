from django.shortcuts import render

# Create your views here.
def show_podcast(request):
    content = {
        "podcasts": [
            {
                "title": "Joe Rogan Experience",
                "genre": "Comedy",
                "podcaster": "Joe Rogan",
                "durasi": "200 jam",
                "tanggal": "10/08/22",
                "episodes": [
                    {
                        "judul": "JRE #102",
                        "deskripsi": "Podcast with x",
                        "durasi_episode": "2 jam 10 menit",
                        "tanggal_episode": "16/04/2023"
                    },
                    {
                        "judul": "JRE #103",
                        "deskripsi": "Podcast with y",
                        "durasi_episode": "2 jam 15 menit",
                        "tanggal_episode": "23/04/2023"
                    },
                    {
                        "judul": "JRE #104",
                        "deskripsi": "Podcast with z",
                        "durasi_episode": "1 jam 45 menit",
                        "tanggal_episode": "30/04/2023"
                    }
                ]
            },
            {
                "title": "Bad Friends Podcast",
                "genre": "Comedy",
                "podcaster": "Andrew Santino",
                "durasi": "150 jam",
                "tanggal": "15/09/21",
                "episodes": [
                    {
                        "judul": "Episode #1",
                        "deskripsi": "Interview with A",
                        "durasi_episode": "1 jam 30 menit",
                        "tanggal_episode": "05/05/2023"
                    },
                    {
                        "judul": "Episode #2",
                        "deskripsi": "Interview with B",
                        "durasi_episode": "2 jam",
                        "tanggal_episode": "12/05/2023"
                    },
                    {
                        "judul": "Episode #3",
                        "deskripsi": "Interview with C",
                        "durasi_episode": "1 jam 45 menit",
                        "tanggal_episode": "19/05/2023"
                    }
                ]
            },
            {
                "title": "Chunkz & Filly Show",
                "genre": "Comedy",
                "podcaster": "Chunkz",
                "durasi": "80 jam",
                "tanggal": "20/03/20",
                "episodes": [
                    {
                        "judul": "Season 1, Episode 1",
                        "deskripsi": "Debunking topic X",
                        "durasi_episode": "45 menit",
                        "tanggal_episode": "25/05/2023"
                    },
                    {
                        "judul": "Season 1, Episode 2",
                        "deskripsi": "Exploring topic Y",
                        "durasi_episode": "1 jam",
                        "tanggal_episode": "01/06/2023"
                    },
                    {
                        "judul": "Season 1, Episode 3",
                        "deskripsi": "Investigating topic Z",
                        "durasi_episode": "1 jam 15 menit",
                        "tanggal_episode": "08/06/2023"
                    }
                ]
            }
        ]
    }

    return render(request, 'play_podcast.html', content)