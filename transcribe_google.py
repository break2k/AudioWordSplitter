import sys, os, logging, datetime
from pydub import AudioSegment
from google.cloud import speech

# file input
audio_file_path = sys.argv[1]

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def transcribe_audio_with_google(audio_file_path):
    client = speech.SpeechClient()

    with open(audio_file_path, 'rb') as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=44100,
        language_code='en-US',
        enable_word_time_offsets=True,
        audio_channel_count = 2,
        max_alternatives=3,
        enable_automatic_punctuation=True,
        model='video',
        enable_separate_recognition_per_channel=True        
    )

    response = client.recognize(config=config, audio=audio)

    words = []
    for result in response.results:
        for alternative in result.alternatives:
            for word_info in alternative.words:
                word = word_info.word
                start_time = word_info.start_time.total_seconds()
                end_time = word_info.end_time.total_seconds()
                logging.debug("Word: %s, Start time: %s, End time: %s", word, start_time, end_time)
                words.append((word, start_time, end_time))

    return words

def split_audio(audio_file_path, words):
    logging.info(f"Loading audio file: {audio_file_path}")
    audio = AudioSegment.from_file(audio_file_path)
    
    base_filename = os.path.splitext(audio_file_path)[0]

    for i, (word, start_time, end_time) in enumerate(words):
        start_ms = int(start_time * 1000)
        end_ms = int(end_time * 1000)
        word_audio = audio[start_ms:end_ms]
        word_filename = f"output/google/{word}_{i+1}.wav"
        logging.info(f"Exporting word: {word_filename}, Start time: {start_ms} ms, End time: {end_ms} ms")
        word_audio.export(word_filename, format="wav")
        logging.debug(f"Exported: {word_filename}")

# Transcribe the audio to get words and timestamps
logging.info("Starting transcription process...")
words = transcribe_audio_with_google(audio_file_path)

# Split the audio based on the transcription
logging.info("Starting audio splitting process...")
split_audio(audio_file_path, words)

logging.info("Process completed.")