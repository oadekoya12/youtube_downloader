#!/usr/bin/env python3
import os
import sys
import argparse
import whisper
import ffmpeg

def extract_audio(input_video_path, output_audio_path):
    """Extract audio from a video file using ffmpeg."""
    input_abs = os.path.abspath(input_video_path)
    output_abs = os.path.abspath(output_audio_path)
    print(f"[DEBUG] Extracting audio from: {input_abs}")
    print(f"[DEBUG] Audio output will be saved to: {output_abs}")

    # Check if the input file exists
    if not os.path.exists(input_abs):
        print(f"[ERROR] Input file does not exist: {input_abs}", file=sys.stderr)
        sys.exit(1)

    try:
        ffmpeg.input(input_abs).output(output_abs, ac=1, ar=16000).run(overwrite_output=True)
    except ffmpeg.Error as e:
        # Safely decode stderr if it exists
        err_msg = e.stderr.decode() if e.stderr is not None else "No error message available"
        print(f"[ERROR] FFmpeg error for {input_abs}: {err_msg}", file=sys.stderr)
        raise


def transcribe_file(file_path, model):
    """Transcribe a single video file and save the transcript as a text file."""
    file_abs = os.path.abspath(file_path)
    print(f"[DEBUG] Processing file: {file_abs}")
    if not os.path.isfile(file_abs):
        print(f"[ERROR] File does not exist: {file_abs}", file=sys.stderr)
        return
    base, _ = os.path.splitext(file_abs)
    audio_path = base + ".wav"
    try:
        extract_audio(file_abs, audio_path)
    except Exception as e:
        print(f"[ERROR] Error extracting audio from {file_abs}: {e}", file=sys.stderr)
        return
    try:
        result = model.transcribe(audio_path)
    except Exception as e:
        print(f"[ERROR] Error transcribing audio for {file_abs}: {e}", file=sys.stderr)
        return
    transcript = result.get("text", "").strip()
    transcript_file = base + ".txt"
    with open(transcript_file, "w", encoding="utf-8") as f:
        f.write(transcript)
    print(f"[INFO] Transcript saved to {transcript_file}")

def process_directory(directory, model):
    """Recursively process all video files in a directory."""
    directory_abs = os.path.abspath(directory)
    print(f"[DEBUG] Processing directory: {directory_abs}")
    if not os.path.isdir(directory_abs):
        print(f"[ERROR] The provided path '{directory_abs}' is not a directory.", file=sys.stderr)
        sys.exit(1)
    video_extensions = (".mp4", ".mkv", ".avi", ".mov", ".flv", ".wmv")
    found_files = False
    for root, _, files in os.walk(directory_abs):
        for file in files:
            if file.lower().endswith(video_extensions):
                found_files = True
                file_path = os.path.join(root, file)
                transcribe_file(file_path, model)
    if not found_files:
        print(f"[WARN] No video files found in directory: {directory_abs}")

def main():
    parser = argparse.ArgumentParser(
        description="Transcribe video files using OpenAI Whisper."
    )
    parser.add_argument(
        "mode",
        choices=["file", "directory"],
        help="Mode: 'file' to transcribe a single file, 'directory' to process all video files in a directory"
    )
    parser.add_argument(
        "path",
        help="Path to the video file or directory containing video files"
    )
    parser.add_argument(
        "--model",
        default="base",
        help="Whisper model to use (tiny, base, small, medium, large). Default is 'base'."
    )
    args = parser.parse_args()

    # Debug: Print received arguments
    print(f"[DEBUG] Arguments received: mode={args.mode}, path={args.path}, model={args.model}")

    if not os.path.exists(args.path):
        print(f"[ERROR] The specified path '{args.path}' does not exist.", file=sys.stderr)
        sys.exit(1)

    print(f"[INFO] Loading Whisper model: {args.model}...")
    model = whisper.load_model(args.model)
    print("[INFO] Model loaded successfully.")

    if args.mode == "file":
        transcribe_file(args.path, model)
    elif args.mode == "directory":
        process_directory(args.path, model)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
