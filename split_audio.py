from pydub import AudioSegment
import io, os, sys, logging

# file input
file_path = sys.argv[1]

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def split_wav_file(file_path, output_dir, segment_length_ms=50000):
    # Load the audio file
    audio = AudioSegment.from_wav(file_path)
    
    # Get the duration of the audio file in milliseconds
    audio_length_ms = len(audio)
    
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Split the audio into segments
    for start_ms in range(0, audio_length_ms, segment_length_ms):
        end_ms = start_ms + segment_length_ms
        segment = audio[start_ms:end_ms]
        
        # Create a filename for each segment
        segment_filename = os.path.join(output_dir, f'segment_{start_ms // 1000 // 60:02}_{(start_ms // 1000) % 60:02}.wav')
        
        # Export the segment
        segment.export(segment_filename, format='wav')
        logging.info(f'Saved segment: {segment_filename}')

# Example usage
output_dir = 'output/segments'
split_wav_file(file_path, output_dir)