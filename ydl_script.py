import json
import yt_dlp
import argparse
import os
import pytube
import pandas as pd
import subprocess

parser = argparse.ArgumentParser(description='Youtube download configurations', add_help=False)
parser.add_argument('--youtube-link-video', type=str, help='Direct link of youtube video')
parser.add_argument('--youtube-json-videos', type=str, help='Extracted Youtube videos json list')

parser.add_argument('--op-format', type=str, default='audio', choices=['video', 'audio', 'images'])
parser.add_argument('--op-folder', type=str, default='./data', help='Output folder path')

parser.add_argument('--to-wav-format', action='store_true', help='Convert files to wav format for lossless '
                                                                 'compression files')

args = parser.parse_args()

assert args.youtube_link_video is None or args.youtube_json_videos is None, 'You should either provide a ' \
                                                                            'youtube video link or youtube ' \
                                                                            'videos json file '

assert args.op_format == 'audio' or args.op_format == 'video' or args.op_format == 'images', 'Only audio, images and ' \
                                                                                             'video formats are ' \
                                                                                             'supported '

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

def download_yt_video(video_link, output_folder, format, to_wav):
    video_yt = pytube.YouTube(video_link)
    try:
        video_yt.check_availability()
    except pytube.exceptions.VideoUnavailable:
        raise (RuntimeError(f"{video_link} isn't available."))

    video_title = video_yt.title.replace('/', '_').replace('\\', '_').replace(' ', '_').replace('|', '_').replace('~', '_').replace('!', '_')
    print(video_title)
    if format == 'audio':

        video_yt.streams.filter(file_extension='mp4', only_audio=True).first().download(
            output_path=output_folder,
            filename=f"{video_title}.mp4"
        )

        if to_wav:
            # Converting the file to wav format to have a very good quality file before processing
            result = subprocess.run(
                ["ffmpeg", "-i", f"{output_folder}/{video_title}.mp4", "-vn", "-acodec", "pcm_s16le", "-ar", "16000",
                 "-ac", "1", f"{output_folder}/{video_title}.wav"])

    elif format == 'images':
        video_yt.streams.filter(file_extension='mp4', only_video=True).order_by('resolution').desc().first().download(
            output_path=output_folder,
            filename=f"{video_title}.mp4"
        )
    elif format == 'video':
        video_yt.streams.filter(file_extension='mp4').order_by('resolution').desc().first().download(
            output_path=output_folder,
            filename=f"{video_title}.mp4"
        )


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
        download_yt_video(video['link'], args.op_folder, args.op_format, args.to_wav_format)

    df = pd.DataFrame(data_info, columns={'Titles', 'Links', 'Url_page'})
    df.to_csv(f"{args.op_folder}/info.csv", index=False)
else:
    # Download only one YouTube video
    # download_youtube_video(args.youtube_link_video, my_hook, args.op_folder, args.op_format)
    download_yt_video(args.youtube_link_video, args.op_folder, args.op_format, args.to_wav_format)
