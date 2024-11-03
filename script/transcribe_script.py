import whisper
import ffmpeg
import os
import sys

def extract_audio(input_video_path, output_audio_path):
    """Extracts audio from the video file using ffmpeg."""
    try:
        # Extract audio
        ffmpeg.input(input_video_path).output(output_audio_path, ac=1, ar=16000).run(overwrite_output=True)
        print(f"Audio extracted to {output_audio_path}")
    except ffmpeg.Error as e:
        print("FFmpeg error:", e.stderr.decode())
        sys.exit(1)

def transcribe_audio(audio_path, output_text_path):
    """Transcribes audio to text using Whisper and saves the text."""
    try:
        model = whisper.load_model("base")
        result = model.transcribe(audio_path)
        text = result["text"]
        
        # Save transcript
        with open(output_text_path, 'w') as f:
            f.write(text)
        
        print(f"Transcription saved to {output_text_path}")
    except Exception as e:
        print(f"Transcription error: {e}")
        sys.exit(1)

def main(input_video_path):
    base_name = os.path.splitext(input_video_path)[0]
    audio_path = f"{base_name}_audio.wav"
    transcript_path = f"{base_name}_transcript.txt"
    
    extract_audio(input_video_path, audio_path)
    transcribe_audio(audio_path, transcript_path)

    # Clean up audio file if desired
    os.remove(audio_path)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python transcribe_script.py <path_to_video>")
        sys.exit(1)
    
    input_video_path = sys.argv[1]
    main(input_video_path)
