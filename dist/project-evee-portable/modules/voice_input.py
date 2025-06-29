import pyaudio
import wave
import numpy as np

#recording audio
def record_audio(filename, rate=16000, channels=1):
    
    silence_limit = 4  # 2 seconds of silence before stopping
    # compute how many blocks constitute the max duration & silence limit
    max_blocks     = int(rate / 1024 * 90)  # 30 seconds maximum recording time
    silent_blocks  = int(rate / 1024 * silence_limit)

    p = pyaudio.PyAudio()

    #open the stream
    stream = p.open(format=pyaudio.paInt16, channels=channels, rate=rate, input=True, frames_per_buffer=1024)
    print("Recording... (Speak now, recording will stop after you finish talking)")

    silence_counter = 0
    speaking = False  # Track if we've started speaking

    #recording
    frames = []
    for i in range(max_blocks):
        data = stream.read(1024, exception_on_overflow=False)
        frames.append(data)

        # 1) compute RMS or mean absolute amplitude
        audio_block = np.frombuffer(data, dtype=np.int16)
        amplitude = np.abs(audio_block).mean()

        if amplitude < 300:  # Reduced threshold from 500 to 300
            if speaking:  # Only count silence if we've started speaking
                silence_counter += 1
        else:
            speaking = True  # We've detected speech
            silence_counter = 0

        # 2) if we've seen enough consecutive "quiet" frames, break
        if silence_counter > silent_blocks:
            print(f"Silence detected for {silence_limit}s → stopping")
            break
    
    #clean up
    stream.stop_stream()
    stream.close()
    p.terminate()

    #save the recording into the filename passed
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(rate)
        wf.writeframes(b''.join(frames))
    print(f"Audio recorded and saved as: {filename}")

    return filename

