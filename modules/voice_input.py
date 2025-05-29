import pyaudio
import wave

# 1. open the microphone stream
def record_with_pyaudio(output_filename, duration=5, format=pyaudio.paInt16, channels=1, rate=44100):
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)

    print("Recording...")
    frames = []

    # 2. record the audio
    for i in range(0, int(rate / 1024 * duration)):
        data = stream.read(1024)
        frames.append(data)

    # 3. stop the stream
    stream.stop_stream()    
    stream.close()

    # 4. save the audio to a WAV file
    with wave.open(output_filename, "wb") as wav_file:
        wav_file.setnchannels(channels)
        wav_file.setsampwidth(2)
        wav_file.setframerate(rate)
        wav_file.writeframes(b''.join(frames))

    return "output.wav"

