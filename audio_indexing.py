import subprocess
from pathlib import Path
from tkinter import Tk, filedialog
import speech_recognition as sr
from os import path

# Constants for non-text segments
STARTING_SEGMENT = '<s>'
ENDING_SEGMENT = '</s>'
SYLLABLE_SEGMENT = '<sil>'
NON_TEXT_SEGMENTS = [STARTING_SEGMENT, ENDING_SEGMENT, SYLLABLE_SEGMENT]


# Step 1: Select a video file and extract audio
def extract_audio_from_video():
    Tk().withdraw()
    video_path = filedialog.askopenfilename(
        title="Select a video file",
        filetypes=[("Video files", "*.mp4 *.3gp *.3gpp *.avi *.mov *.mkv")]
    )

    if not video_path:
        raise ValueError("No video file selected.")

    video_file = Path(video_path)
    if not video_file.exists():
        raise FileNotFoundError(f"Video not found: {video_file}")

    output_file = video_file.with_suffix(".wav")

    cmd = [
        "ffmpeg", "-y",
        "-i", str(video_file),
        "-vn", "-ac", "2", "-ar", "44100", "-b:a", "160k",
        str(output_file)
    ]
    subprocess.run(cmd, check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    print(f"Audio extracted: {output_file}")
    return output_file


# Step 2: Read audio into SpeechRecognition
def get_audio_data(audio_file_name):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file_name) as source:
        audio_data = recognizer.record(source)
    return audio_data


# Step 3a: Convert audio to full text
def get_text_from_audio(audioData):
    r = sr.Recognizer()
    text = ''
    try:
        text = r.recognize_sphinx(audioData)
        print("\n--- Transcribed Text ---")
        print(text)
    except sr.UnknownValueError:
        print("Sphinx could not understand audio")
    except sr.RequestError as e:
        print("Sphinx error;", e)
    return text


# Step 3b: Get segments with timestamps
def get_text_segments_from_audio(audioData):
    r = sr.Recognizer()
    segments = {}
    try:
        decoder = r.recognize_sphinx(audioData, show_all=True)
        for seg in decoder.seg():
            if seg.word not in NON_TEXT_SEGMENTS:
                time_frame = (seg.start_frame / 100, seg.end_frame / 100)
                if seg.word in segments:
                    segments[seg.word].append(time_frame)
                else:
                    segments[seg.word] = [time_frame]
    except sr.UnknownValueError:
        print("Sphinx could not understand audio")
    except sr.RequestError as e:
        print("Sphinx error;", e)
    return segments


# Step 4: Play audio from a selected index until user stops
def play_audio_from_index(input_wav, start_time):
    command = [
        "ffplay", "-nodisp", "-autoexit",
        "-ss", str(start_time),
        str(input_wav)
    ]
    subprocess.Popen(command,
                     stdout=subprocess.DEVNULL,
                     stderr=subprocess.DEVNULL)

# Main execution
if __name__ == "__main__":
    # Step 1: Extract audio
    output_file = extract_audio_from_video()

    # Step 2: Load audio data
    audioData = get_audio_data(str(output_file))

    # Step 3: Get transcription
    entire_text = get_text_from_audio(audioData)
    print(f"\nEntire text for {output_file}:\n{entire_text}\n")

    # Step 3: Get word segments
    segments = get_text_segments_from_audio(audioData)

    # Ask user for word
    key = input("Enter a word to check its occurrences: ").lower()
    if key in segments:
        frames = segments[key]
        num_times = len(frames)
        for i, frame in enumerate(frames, start=1):
            print(f"[{i}] {key} -> starts at {frame[0]}s, ends at {frame[1]}s")

        choice = input(
            "Enter the index number to play from that occurrence (or press Enter to skip): "
        )
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(frames):
                start, end = frames[idx]
                print(f"\nPlaying from {start}s. Press 'q' in the ffplay window to stop.\n")
                play_audio_from_index(output_file, start)
            else:
                print("Invalid index selected.")
    else:
        print(f"The word [{key}] not found in the audio file.")
