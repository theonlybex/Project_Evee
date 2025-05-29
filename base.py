# base.py

import os
from pathlib import Path
import warnings

# ——————————————————————————————————————————————
# 1) Bundle in the imageio-ffmpeg binary so Whisper finds it
# ——————————————————————————————————————————————
import imageio_ffmpeg as iioffmpeg

ffmpeg_exe = iioffmpeg.get_ffmpeg_exe()
ffmpeg_dir = os.path.dirname(ffmpeg_exe)
os.environ["PATH"] = ffmpeg_dir + os.pathsep + os.environ.get("PATH", "")

# ——————————————————————————————————————————————
# 2) Suppress that FP16 warning when running on CPU
# ——————————————————————————————————————————————
warnings.filterwarnings("ignore", message="FP16 is not supported on CPU")

# ——————————————————————————————————————————————
# 3) Your modules & imports
# ——————————————————————————————————————————————
from modules.voice_input import record_with_pyaudio
import whisper

def main():
    # Determine paths relative to this script
    SCRIPT_DIR   = Path(__file__).parent
    OUTPUT_WAV   = SCRIPT_DIR / "recording.wav"
    OUTPUT_TXT   = SCRIPT_DIR / "transcription.txt"

    # ——————————————————————————————————————————————
    # 4) Record audio
    # ——————————————————————————————————————————————
    print("Starting recording (5s)...")
    wav_path = record_with_pyaudio(
        output_filename=str(OUTPUT_WAV),
        duration=5,
        rate=16000       # Whisper expects 16 kHz
    )
    print(f"✅ Saved recording to: {wav_path}")

    # Sanity-check
    if not OUTPUT_WAV.exists():
        raise FileNotFoundError(f"No file at {OUTPUT_WAV}")
    if OUTPUT_WAV.stat().st_size == 0:
        raise ValueError(f"File is empty: {OUTPUT_WAV}")

    # ——————————————————————————————————————————————
    # 5) Load Whisper & transcribe
    # ——————————————————————————————————————————————
    print("Loading Whisper model…")
    model = whisper.load_model("base")

    print("Transcribing…")
    result = model.transcribe(str(OUTPUT_WAV))
    text = result["text"].strip()
    print("🎙 You said:", text)

    # ——————————————————————————————————————————————
    # 6) Save transcription
    # ——————————————————————————————————————————————
    with open(OUTPUT_TXT, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"✅ Transcription saved to: {OUTPUT_TXT}")

if __name__ == "__main__":
    main()
