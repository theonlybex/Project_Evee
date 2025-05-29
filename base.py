import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import whisper

# Transcribe
print("Transcribing...")
model = whisper.load_model("base")
result = model.transcribe("recording.wav")
transcribed_text = result["text"]
print("You said:", transcribed_text)