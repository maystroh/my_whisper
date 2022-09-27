# https://github.com/alexmercerind/youtube-search-python
from youtubesearchpython import *
import json


name_playlist = 'Lex Friedman Podcast'
playlist_url = 'https://www.youtube.com/playlist?list=PLrAXtmErZgOdP_8GztsuKi9nrraNbKKp4'

playlist = Playlist(playlist_url)

print(f'Videos Retrieved: {len(playlist.videos)}')

playlistVideos = playlist.getVideos(playlist_url)
# print(playlistVideos)

videos_play = playlistVideos['videos']

while playlist.hasMoreVideos:

    print('Getting more videos...')
    playlist.getNextVideos()
    print(f'Videos Retrieved: {len(playlist.videos)}')

# Serializing json
json_object = json.dumps(playlist.videos, indent=4)
with open(f"{name_playlist}_videos.json", "w") as outfile:
    outfile.write(json_object)


print('Found all the videos.')