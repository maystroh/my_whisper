import whisper
import argparse
import glob
import tqdm

# python whisper_audio_to_text.py --path-folder=data

parser = argparse.ArgumentParser(description='Whisper simple usage', add_help=False)
parser.add_argument('--whisper-model', type=str, default='small', choices=['tiny', 'base', 'small', 'medium', 'large'])
parser.add_argument('--path-file', type=str, help='path of the audio file to transcribe')
parser.add_argument('--path-folder', type=str, help='Transcribe the audio files in this folder')
parser.add_argument('--extension', type=str, default='wav', help='Extension of the files to be transcribed')
parser.add_argument('--transcribe-whole-files', action='store_true', help='Transcribe the whole audio file(s)')
args = parser.parse_args()

if args.path_folder is not None:
    # glob all files ending with mp3 extension
    audio_files = glob.glob(f'{args.path_folder}/*.{args.extension}')
else:
    audio_files = [args.path_file]

assert len(audio_files) > 0, 'Please specify a path for a folder or a file to process'

model = whisper.load_model(args.whisper_model)

for path_file in tqdm.tqdm(audio_files):
    print(path_file)

    if args.transcribe_whole_files:
        result = model.transcribe(path_file)
        extracted_text = result['text']
        name_of_transcribed_file = f"{path_file}_transcribed.txt"
    else:
        # load audio and pad/trim it to fit 30 seconds
        audio = whisper.load_audio(path_file)
        audio = whisper.pad_or_trim(audio)

        # make log-Mel spectrogram and move to the same device as the model
        mel = whisper.log_mel_spectrogram(audio).to(model.device)

        # detect the spoken languagem
        _, probs = model.detect_language(mel)
        print(f"Detected language: {max(probs, key=probs.get)}")

        # decode the audio
        options = whisper.DecodingOptions()
        result = whisper.decode(model, mel, options)

        # print the recognized text
        print(result.text)
        extracted_text = result.text
        name_of_transcribed_file = f"{path_file}_30sec.txt"

    with open(name_of_transcribed_file, "w") as f:
        f.write(extracted_text)
