import pyaudio
import wave

# 1. open the microphone stream
def record_with_pyaudio(output_filename, duration=5, format=pyaudio.paInt16, channels=1, rate=16000):
    p = pyaudio.PyAudio()
    stream = p.open(format=format, channels=channels, rate=rate, input=True, frames_per_buffer=1024)

    print(f"Recording to {output_filename} for {duration} seconds")
    frames = []

    # 2. record the audio
    for i in range(0, int(rate / 1024 * duration)):
        data = stream.read(1024)
        frames.append(data)

    # 3. stop the stream
    stream.stop_stream()    
    stream.close()
    p.terminate()

    # 4. save the audio to a WAV file
    with wave.open(output_filename, "wb") as wav_file:
        wav_file.setnchannels(channels)
        wav_file.setsampwidth(p.get_sample_size(format))
        wav_file.setframerate(rate)
        wav_file.writeframes(b"".join(frames))

    #return output_file with audio
    return output_filename

