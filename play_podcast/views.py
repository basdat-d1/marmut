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
                        "deskripsi": "Podcast with Theo Von",
                        "durasi_episode": "2 jam 10 menit",
                        "tanggal_episode": "16/04/2023"
                    },
                    {
                        "judul": "JRE #103",
                        "deskripsi": "Podcast with Max Holloway",
                        "durasi_episode": "2 jam 15 menit",
                        "tanggal_episode": "23/04/2023"
                    },
                    {
                        "judul": "JRE #104",
                        "deskripsi": "Podcast with Joey Diaz",
                        "durasi_episode": "1 jam 45 menit",
                        "tanggal_episode": "30/04/2023"
                    }
                ]
            },
        ]
    }

    return render(request, 'play_podcast.html', content)