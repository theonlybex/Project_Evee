import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import whisper
from deepseek import DeepSeek  # Add DeepSeek import

# Initialize DeepSeek client
deepseek = DeepSeek(api_key="YOUR_API_KEY")  # Replace with your actual API key

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
transcribed_text = result["text"]
print("You said:", transcribed_text)

# Send to DeepSeek API
print("Sending to DeepSeek API...")
response = deepseek.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "user", "content": transcribed_text}
    ]
)
print("DeepSeek response:", response.choices[0].message.content)