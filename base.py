import os
import imageio_ffmpeg as ffmpeg

# Ensure our bundled ffmpeg is used
ffmpeg_exe = ffmpeg.get_ffmpeg_exe()
ffmpeg_dir = os.path.dirname(ffmpeg_exe)
os.environ["PATH"] = ffmpeg_dir + os.pathsep + os.environ.get("PATH", "")


import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import whisper
import modules.voice_input as voice_input
import warnings
import os

# Suppress the FP16 warning
warnings.filterwarnings("ignore", message="FP16 is not supported on CPU")

# Recording now
output_file = "recording.wav"
voice_input.record_with_pyaudio(output_file)

# Check if file exists and has content
if not os.path.exists(output_file):
    raise FileNotFoundError(f"Recording file {output_file} was not created")
if os.path.getsize(output_file) == 0:
    raise ValueError(f"Recording file {output_file} is empty")

print(f"Recording saved to {output_file}")

# Transcribe
print("Transcribing...")
try:
    model = whisper.load_model("base")
    result = model.transcribe("recording.wav")
    transcribed_text = result["text"]
    print("You said:", transcribed_text)

    # Write transcribed text to a file
    with open("transcription.txt", "w", encoding="utf-8") as f:
        f.write(transcribed_text)
    print("Transcription saved to transcription.txt")
except Exception as e:
    print(f"Error during transcription: {str(e)}")
    raise