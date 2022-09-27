import json
import yt_dlp



def my_hook(d):
    if d['status'] == 'finished':
        print('\nDone downloading, now converting ...')


# Opening JSON file
f = open('Lex Friedman Podcast_videos.json')
  
# returns JSON object as a dictionary
data = json.load(f)

for video in data:
    print(video['title'])
    print(video['link'])

    # ydl_opts = {
    #     'format': 'mp3',       
    #     'outtmpl': video['title'],        
    #     'noplaylist' : True,        
    #     'progress_hooks': [my_hook],  
    # }

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f"./data/{video['title']}.mp3", 
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'noplaylist' : True,
        'progress_hooks': [my_hook], 
    }


    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        error_code = ydl.download([video['link']])

    break