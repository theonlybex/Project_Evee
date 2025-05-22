import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import whisper

# Record audio
print("Recording... Speak now!")
duration = 5  # seconds
fs = 44100  # sample rate
recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
sd.wait()  # Wait until recording is finished
print("Recording finished!")

# Save the recording
write("recording.wav", fs, recording)
print("Saved to recording.wav")

# Transcribe
print("Transcribing...")
model = whisper.load_model("base")
result = model.transcribe("recording.wav")
print("You said:", result["text"])