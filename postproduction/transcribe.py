# postproduction/transcribe.py
import argparse
import os
import whisper

def transcribe(input_path, output_path=None, model_size="medium"):
    model = whisper.load_model(model_size)
    result = model.transcribe(input_path)

    output_path = output_path or input_path.rsplit(".", 1)[0] + ".txt"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(result["text"])

    print(f"[✓] Transcript saved to {output_path}")
    return output_path

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Path to video/audio file")
    parser.add_argument("--output", help="Optional path to save transcript")
    parser.add_argument("--model", default="medium", help="Whisper model (tiny, base, small, medium, large)")
    args = parser.parse_args()

    transcribe(args.input, args.output, args.model)
