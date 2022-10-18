import argparse
import glob
import subprocess

# python whisper_command.py --path-folder=yt_Letitia_transformers --extension=mp3 --whisper-model=small --task=transcribe --language=en

parser = argparse.ArgumentParser(description='Whisper simple usage', add_help=False)
parser.add_argument('--whisper-model', type=str, default='small', choices=['tiny', 'base', 'small', 'medium', 'large'])
parser.add_argument('--path-file', type=str, help='path of the audio file to transcribe/translate')
parser.add_argument('--path-folder', type=str, help='Transcribe/translate the audio files in this folder')
parser.add_argument('--extension', type=str, default='wav', help='Extension of the files to be transcribed/translate')
parser.add_argument('--task', type=str, default='transcribe', choices=["transcribe", "translate"])
parser.add_argument('--language', type=str, default='en')

args = parser.parse_args()

if args.path_folder is not None:
    # glob all files ending with mp3 extension
    audio_files = glob.glob(f'{args.path_folder}/*.{args.extension}')
else:
    audio_files = [args.path_file]

assert len(audio_files) > 0, 'Please specify a path for a folder or a file to process'

command_to_launch = 'whisper '
command_to_launch = command_to_launch + ' '.join(audio_files) + ' --model=' + args.whisper_model + ' --task=' + \
                    args.task + ' --language=' + args.language + ' --output_dir=' + args.path_folder
print(command_to_launch)

subprocess.call(command_to_launch, shell=True)
