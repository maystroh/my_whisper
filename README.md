# My_whisper (OpenAI)
This is just my version of whisper. For deep understanding of whisper, we refer the reader to the [official page of Whisper](https://github.com/openai/whisper). To test these models, we just added files to fetch/download Youtube videos:

In case you work with a playlist or channel, here is how to get their information:

``python youtube_search.py --playlist-url=https://www.youtube.com/playlist?list=PLpZBeKTZRGPMddKHcsJAOIghV8MwzwQV6 --playlist-name=yt_Letitia_transformers``

We can either download a Youtube video by its url or a playlist (channel) by the json file generated from the previous command:

``python ydl_script.py --op-format=audio --op-folder=yt_Letitia_transformers  --youtube-json-videos=yt_Letitia_transformers_videos.json ``

Then, to get the audio files transcribed, we launch the following command:

``python whisper_audio_to_text.py --path-folder=yt_Letitia_transformers/ --transcribe-whole-files``.

It actually reads the audio files in the folder `yt_Letitia_transformers` and transcribes then into a `txt` file 

OR use `Whisper` API:

``whisper audio.mp3 --model medium``

### Notebook
In a latest update on `Whisper` main repository, they added a notebook called `Youtube_ASR`. Please use it to download and transcribe/translate any Youtube video.

### HTML page
Inspired by [Karpathy tweet](https://twitter.com/karpathy/status/1574501715990102016), we generate web pages listing the videos with the generated text. We use ``generate_html_content`` script to generate the body of a template html page we have. Please check `letitiatransformers.html` to see an example.


