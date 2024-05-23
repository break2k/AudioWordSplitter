import logging
import sys
from pydub import AudioSegment
import requests
import whisper

# file input
audio_file_input = sys.argv[1]

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)


# Transcribe audio using Whisper
def transcribe_audio_with_whisper(audio_file_path):
    model = whisper.load_model("base")
    result = model.transcribe(audio_file_path, fp16=False)
    transcription = result["text"]
    return transcription


# Align transcription using Gentle hosted locally in Docker
def align_with_gentle_docker(audio_file_path, transcription):
    url = "http://localhost/transcriptions?async=false"
    files = {"audio": open(audio_file_path, "rb"), "transcript": (None, transcription)}

    response = requests.post(url, files=files, timeout=10)
    response.raise_for_status()  # Raise an error if the request failed

    alignment = response.json()
    return alignment


# Split audio using word timestamps from Gentle
def split_audio(audio_file_path, alignment):
    audio = AudioSegment.from_file(audio_file_path)

    for i, word_info in enumerate(alignment["words"]):
        if word_info["case"] == "success":
            word = word_info["alignedWord"]
            start_time = word_info["start"]
            end_time = word_info["end"]

            start_ms = int(start_time * 1000)
            end_ms = int(end_time * 1000)

            word_audio = audio[start_ms:end_ms]
            word_filename = f"output/whisper_gentle/{word}_{i+1}.wav"
            word_audio.export(word_filename, format="wav")
            logging.info("Exported: %s", word_filename)


# Main script execution
def main():
    # Transcribe the audio with Whisper
    logging.info("Starting transcription with Whisper...")
    transcription = transcribe_audio_with_whisper(audio_file_input)

    # Align the transcription with Gentle hosted in Docker
    logging.info("Starting alignment with Gentle...")
    alignment = align_with_gentle_docker(audio_file_input, transcription)

    # Split the audio based on Gentle's alignment
    logging.info("Starting audio splitting...")
    split_audio(audio_file_input, alignment)
    logging.info("Process completed.")


if __name__ == "__main__":
    main()
