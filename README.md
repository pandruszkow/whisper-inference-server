# whisper-inference-server
An inference server for Whisper so you don't have to keep waiting for the audio model to reload for the x-hunderdth time.

## Installation

Clone the repository, and then run the following to install and run this in a venv.

```sh
virtualenv .
source bin/activate
pip install -r requirements.txt 
python3 whisper_inference_server.py 
```

You should be fine provided that Whisper itself works fine on your machine. Make sure that CUDA is detected if you want to use that.

## How to use (endpoints)

By default, this will listen on http://127.0.0.1:5000. The following endpoints are available on that port:

* `/`: shows a plain HTML+JS page that can be used as a demo. Use the file picker to provide an audio file, click submit, and then wait until you see the transcription.
  * You will need to wait for the file to process fully before seeing anything, so be patient if it's taking a while.

* `/recognise`: this is what you want if you're going to be programming against this server. This endpoint accepts an audio file, transcribes it into a JSON response, and returns that. You get exactly the kind of object you would get from Whisper's Python API.
  * The transcription result JSON is pretty large and detailed, so you probably want just the `text` field unless you're doing something advanced. I'm including all that data to make the transition from Whisper Python API to the Whisper inference server API as invisible as possible. In the future, this level of detail may be optional.
  * **This endpoint is synchronous** for simplicity - it blocks for as long as it takes to produce the transcription, so if you want to be doing other things while this is churning away in the background, then I recommend calling this from a thread.

* `/reload`: change which speech recognition model is used by the subsequent transcription requests.
  * If you do not know what this does, then you don't need to use this.
  * Request format: JSON with a `model_name` field specifying the name of the model to load. Same names as the command line Whisper utility

## Security

This is designed to be deployed on a trusted internal network. Security is non-existent. Add extra layers of security to protect this from outside access.

## Available model sizes

By default, the server starts with the `medium` Whisper model loaded, but it can use every size that the original CLI utility can handle. Quantised models may be added at a later date.

## TODO
* Quantised models to allow loading `large` on <8 GB VRAM
* Security & make this more "productionised" in how it runs - an auth token in the request header should prevent abuse, and some sort of CGI/containerisation support may help
* Docker support + GPU pass-through
* Make detailed transcription JSON an option rather than the default
* Streaming WAV transcription endpoint for real-time speech recognition
* Async endpoint with the concept of "transcription jobs" - might be more suitable for transcribing larger files. See if progress can be included here.

## Credits

Shout out to https://github.com/davabase/whisper_real_time whose code inspired me to do this.
