import os
import whisper
from pathlib import Path

AUDIO_EXTS = ('.mp3', '.wav', '.m4a', '.flac', '.aac', '.ogg', '.mp4')
model = whisper.load_model('base')

def transcribe_audio_files(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(AUDIO_EXTS):
                file_path = os.path.join(root, file)
                print(f'Processing: {file}')
                try:
                    result = model.transcribe(file_path)
                    output_path = os.path.join(root, Path(file).stem + '.txt')
                    with open(output_path, 'w') as f:
                        f.write(result['text'])
                    print(f'Saved transcript: {output_path}')
                except Exception as e:
                    print(f'Error processing {file}: {str(e)}')
                    continue

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        transcribe_audio_files(sys.argv[1])
    else:
        print("Please provide audio directory path")
        exit(1)