# Audio Indexing Tool

This project extracts audio from a video file, converts it to text, creates word indexes with timestamps, and allows playback of audio starting from specific words.

## Features
- Extracts audio from video files using **FFmpeg**.
- Converts audio to text using **CMU Sphinx** (via `speech_recognition`).
- Creates a word index with timestamps for each occurrence.
- Lets users search for a word → shows all occurrences.
- Plays audio from a selected occurrence until stopped.

## Requirements
- Python 3.8+
- FFmpeg installed ([Download here](https://ffmpeg.org/download.html))
- Python packages:
  ```bash
  pip install SpeechRecognition
  pip install pocketsphinx

## Steps
- Clone the repository
- cd audio-indexing
- Run the script: python audio_indexing.py
- Select a video file when prompted (supported: .mp4, .3gp, .3gpp, .avi, .mov, .mkv).
- The program will extract audio from the video and transcribe it.
- Enter a word to search in the transcript.
- The program will list all timestamps where the word occurs.
- Enter the index number of the occurrence, playback starts from that timestamp (press q to stop).

## Example
- Enter a word to check its occurrences: start
- [1] start -> starts at 10.23s, ends at 10.78s
- [2] start -> starts at 40.23s, ends at 42.78s
- Enter the index number to play from that occurrence: 2
- Playing from 10.23s. Press 'q' in the ffplay window to stop.
