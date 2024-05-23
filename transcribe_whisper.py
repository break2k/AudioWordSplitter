import logging
import sys
import whisper
from pydub import AudioSegment

# file input
audio_file_input = sys.argv[1]

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)


def transcribe_audio_with_whisper(audio_file_path):
    logging.info("Loading Whisper model...")
    model = whisper.load_model("base")

    logging.info("Transcribing audio file: %s", audio_file_path)
    result = model.transcribe(audio_file_path, fp16=False)

    words = []
    for segment in result["segments"]:
        segment_text = segment["text"].strip()
        start_time = segment["start"]
        end_time = segment["end"]
        logging.debug(
            "Segment: %s, Start time: %s, End time: %s",
            segment_text,
            start_time,
            end_time,
        )
        words.append((segment_text, start_time, end_time))

    return words


def split_audio(audio_file_path, words):
    audio = AudioSegment.from_wav(audio_file_path)

    for i, (word, start_time, end_time) in enumerate(words):
        start_ms = int(start_time * 1000)
        end_ms = int(end_time * 1000)
        word_audio = audio[start_ms:end_ms]
        word_audio.export(f"output/whisper/{word}_{i+1}.wav", format="wav")


WORDS = transcribe_audio_with_whisper(audio_file_input)

split_audio(audio_file_input, WORDS)
