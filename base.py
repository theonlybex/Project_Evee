import warnings
warnings.filterwarnings("ignore", message="FP16 is not supported on CPU")
import os
from modules import voice_input as recording
import whisper

#main file
if __name__ == "__main__":
    #call for a record
    recording.record_audio("recording.wav")
    
    filename = "recording.wav"
    
    if os.path.exists(filename):
        print(f"{filename} exists.")
        # Transcribe the audio
        model = whisper.load_model("base")
        result = model.transcribe(filename)
        text = result["text"].strip()
        print("Recognized words:", text)
        #Write recognized words to audiototext.txt
        with open("audiototext.txt", "w", encoding="utf-8") as f:
            f.write(text)
        print("Transcription saved to audiototext.txt")
    else:
        print(f"{filename} does not exist.")
