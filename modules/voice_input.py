import pyaudio
import wave

def record_audio(filename, duration=5, rate=16000, channels=1):
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=channels, rate=rate, input=True, frames_per_buffer=1024)
    print("Recording...")
    frames = []
    for _ in range(0, int(rate / 1024 * duration)):
        data = stream.read(1024, exception_on_overflow=False)
        frames.append(data)
    stream.stop_stream()
    stream.close()
    p.terminate()
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(rate)
        wf.writeframes(b''.join(frames))
    print(f"Audio recorded and saved as: {filename}")

