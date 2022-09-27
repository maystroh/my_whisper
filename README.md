# My_whisper (OpenAI)
This is just my version of whisper. For deep understanding of whisper, we refer the reader to the [official page of Whisper](github.com/openai/whisper). 
So far, we just added 3 files:

``youtube_search.py -> it downloads the playlist information of LexFridman podcast ``

``ydl_script.py -> it downloads one of the videos and converts it to a mp3 file ``

Then, to get it transcribed, we launch the following command:

``whisper_audio_to_text.py -> it reads the mp3 file (hardcoded so far) and transcribes it into a file`` 
