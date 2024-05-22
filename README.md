# AudioWordSplitter

## About

This tool takes a `.wav` file and splits it into segments or words in smaller `wav` files.

## How

Run `sh install.sh` to set up a python virtual environment and install its dependencies. Before you run any command be sure to activate the virtual environment via `source .venv/bin/activate`.

## What

`python3 split_audio.py input/dkrap.wav`

Split a bigger wave file into smaller parts to provide Google with smaller file assets (10MB and 1 minute limit)

`python3 transcribe_google.py output/segments/segment_00_00.wav`

Transcribe and split wave files into smaller wave files per word.

`python3 transcribe_whisper.py input/dkrap.wav`

Transcribe and split wave files into smaller wave files per word segment.

`python3 transcribe_whisper_gentle.py input/dkrap.wav`

Transcribe and split wave files into smaller wave files per word with the highest accuracy based on gentle transcripts.

ℹ️ _Info_: Please host a gentle instance (via Docker) on localhost before.