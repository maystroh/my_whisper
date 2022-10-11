from youtubesearchpython import *
import json
import argparse

# How to run this script:
# python youtube_search.py --playlist-url=https://www.youtube.com/playlist?list=PLpZBeKTZRGPMddKHcsJAOIghV8MwzwQV6 --playlist-name=Letitia_Transformers_vision_playlist
# python ydl_script.py --op-format=video --op-folder=Letitia_transformers  --youtube-json-videos=Letitia_Transformers_vision_playlist_videos.json

parser = argparse.ArgumentParser(description='Youtube search configurations', add_help=False)

parser.add_argument('--channel-id', type=str, help='Youtube channel url')
parser.add_argument('--playlist-url', type=str, help='Youtube playlist url')
parser.add_argument('--playlist-name', type=str, help='Youtube playlist name')

args = parser.parse_args()

assert args.channel_id is None or args.playlist_url is None, 'You should either provide a ' \
                                                                            'youtube channel ID or youtube ' \
                                                                            'playlist url '

name_playlist = args.playlist_name
playlist_url = args.playlist_url if args.channel_id is None else playlist_from_channel_id(args.channel_id)

playlist = Playlist(playlist_url)
print(f'Videos Retrieved: {len(playlist.videos)}')

playlistVideos = playlist.getVideos(playlist_url)
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

