import json
import yt_dlp
import argparse
import os
import pandas as pd

parser = argparse.ArgumentParser(description='Youtube download configurations', add_help=False)
parser.add_argument('--youtube-link-video', type=str, help='Direct link of youtube video')
parser.add_argument('--youtube-json-videos', type=str, help='Extracted Youtube videos json list')

parser.add_argument('--op-format', type=str, default='audio', help='video | audio')
parser.add_argument('--op-folder', type=str, default='./data', help='Output folder path')
args = parser.parse_args()

assert args.youtube_link_video is None or args.youtube_json_videos is None, 'You should either provide a ' \
                                                                            'youtube video link or youtube ' \
                                                                            'videos json file '

assert args.op_format == 'audio' or args.op_format == 'video', 'Only audio and video formats are supported'


# class MyLogger:
#     def debug(self, msg):
#         # For compatibility with youtube-dl, both debug and info are passed into debug
#         # You can distinguish them by the prefix '[debug] '
#         if msg.startswith('[debug] '):
#             pass
#         else:
#             self.info(msg)
#
#     def info(self, msg):
#         pass
#
#     def warning(self, msg):
#         pass
#
#     def error(self, msg):
#         print(msg)

def my_hook(d):
    if d['status'] == 'finished':
        print('\nDone downloading, now converting ...')


def get_ydl_options(output_folder, format, progress, video_title=''):
    video_name = video_title if video_title != '' else '%(title)s.%(resolution)s.%(id)s.%(ext)s'
    if format == 'audio':
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f"{output_folder}/{video_name}.mp3",
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            # 'logger': MyLogger(),
            'noplaylist': True,
            'progress_hooks': [progress],
        }
    else:
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=mp4]/mp4+best[height<=480]',
            'outtmpl': f"{output_folder}/{video_name}",
            # 'logger': MyLogger(),
            'noplaylist': True
        }
    return ydl_opts


def download_youtube_video(video_link, progress, output_folder, format, video_title=''):
    ydl_opts = get_ydl_options(output_folder, format, progress, video_title)
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        error_code = ydl.download([video_link])


if not os.path.exists(args.op_folder):
    os.mkdir(args.op_folder)

if args.youtube_json_videos is not None:
    data_info = []
    f = open(args.youtube_json_videos)
    data = json.load(f)
    for video in data:
        print(video['title'])
        print(video['link'])
        data_info.append([video['title'], video['link'], video['link']])
        # download_youtube_video(video['link'], my_hook, args.op_folder, args.op_format, video['title'])

    df = pd.DataFrame(data_info, columns={'Titles', 'Links', 'Url_page'})
    df.to_csv(f"{args.op_folder}/info.csv", index=False)
else:
    # Download only one YouTube video
    download_youtube_video(args.youtube_link_video, my_hook, args.op_folder, args.op_format)
