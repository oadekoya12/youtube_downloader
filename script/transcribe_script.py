import whisper
import ffmpeg
import os
import sys
from pydub import AudioSegment
from pydub.utils import make_chunks

def extract_audio(input_video_path, output_audio_path):
    """Extracts audio from the video file using ffmpeg."""
    try:
        ffmpeg.input(input_video_path).output(output_audio_path, ac=1, ar=16000).run(overwrite_output=True)
        print(f"Audio extracted to {output_audio_path}")
    except ffmpeg.Error as e:
        print("FFmpeg error:", e.stderr.decode())
        sys.exit(1)

def split_audio(audio_path, chunk_length_ms=30000):
    """Splits audio into chunks of specified length in milliseconds."""
    audio = AudioSegment.from_file(audio_path)
    chunks = make_chunks(audio, chunk_length_ms)
    chunk_paths = []
    for i, chunk in enumerate(chunks):
        chunk_path = f"{audio_path}_chunk{i}.wav"
        chunk.export(chunk_path, format="wav")
        chunk_paths.append(chunk_path)
    return chunk_paths

def transcribe_chunk(chunk_path, model):
    """Transcribes a single audio chunk using Whisper."""
    result = model.transcribe(chunk_path)
    text = result["text"]
    print(f"Transcribed chunk {chunk_path}")
    return text

def combine_transcriptions(transcriptions, output_text_path):
    """Combines all transcriptions into one output file."""
    with open(output_text_path, 'w') as f:
        for transcription in transcriptions:
            f.write(transcription + "\n")
    print(f"Combined transcription saved to {output_text_path}")

def main(input_video_path):
    base_name = os.path.splitext(input_video_path)[0]
    audio_path = f"{base_name}_audio.wav"
    transcript_path = f"{base_name}_transcript.txt"

    # Step 1: Extract audio from the video
    extract_audio(input_video_path, audio_path)

    # Step 2: Split audio into chunks
    chunk_paths = split_audio(audio_path)

    # Step 3: Load Whisper model
    model = whisper.load_model("tiny")  # Use a smaller model to conserve memory

    # Step 4: Transcribe each chunk and gather transcriptions
    transcriptions = []
    for chunk_path in chunk_paths:
        transcription = transcribe_chunk(chunk_path, model)
        transcriptions.append(transcription)
        os.remove(chunk_path)  # Clean up the chunk file after transcription

    # Step 5: Combine all transcriptions into a single file
    combine_transcriptions(transcriptions, transcript_path)

    # Clean up the extracted audio file
    os.remove(audio_path)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python transcribe_script.py <path_to_video>")
        sys.exit(1)
    
    input_video_path = sys.argv[1]
    main(input_video_path)
