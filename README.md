# Audio Converter YT

This repository contains a small Python script that converts English speech in an MP3 file to spoken Spanish.
The pipeline uses [OpenAI Whisper](https://github.com/openai/whisper) for transcription, `deep-translator` for translation,
`gTTS` for Spanish text‑to‑speech and `pydub` for audio processing.

## Features
- Splits long audio into manageable chunks.
- Transcribes English audio with Whisper.
- Translates the transcription to Spanish.
- Generates Spanish speech for each chunk.
- Reassembles the Spanish audio into a single MP3 file.

## Requirements
- Python 3.12 or newer
- [FFmpeg](https://ffmpeg.org/) available on your `PATH` (needed by `pydub`)
- The Python dependencies listed in `audiodubbingpython/pyproject.toml`

## Installation
Create a virtual environment and install the package in editable mode:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ./audiodubbingpython
```

## Usage
Place an English MP3 file in the repository or provide its path, then run:

```bash
python audiodubbingpython/main.py
```

By default the script looks for `english_long_audio.mp3` and writes the output to
`spanish_long_audio.mp3`. Edit the bottom of `main.py` or call
`english_mp3_to_spanish_mp3()` directly to process other files.

## Project Layout
```
/
├── README.md
└── audiodubbingpython/
    ├── main.py
    ├── pyproject.toml
    └── uv.lock
```

The entire conversion pipeline is implemented in `audiodubbingpython/main.py`.

## Next Steps
This project is a minimal prototype. Possible improvements include:
- Adding command-line arguments for input and output paths.
- Better error handling and logging.
- Automated tests for the pipeline.
- Packaging as a reusable CLI tool.
