import whisper

name_file = "data/Will Sasso"
path_file = f"{name_file}.mp3"

model = whisper.load_model("small")
transcribe = False

if transcribe:
    result = model.transcribe(path_file)
    print(result)
    extracted_text = result['text']
    name_of_transcribed_file = f"{name_file}_transcribed.txt"
else:
    # load audio and pad/trim it to fit 30 seconds
    audio = whisper.load_audio(name_file)
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
    name_of_transcribed_file = f"{name_file}_30sec.txt"


with open(name_of_transcribed_file, "w") as f:
    f.write(extracted_text)
