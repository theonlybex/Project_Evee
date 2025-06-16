import warnings
warnings.filterwarnings("ignore", message="FP16 is not supported on CPU")
import os
from modules import voice_input as recording
from modules.deepseek_api_engine import DeepSeekAPIEngine
import whisper
import automation_code

#main file
if __name__ == "__main__":
    # Record and transcribe audio
    recording.record_audio("recording.wav")
    filename = "recording.wav"

    if os.path.exists(filename):
        print(f"{filename} exists.")
        # Transcribe the audio
        model = whisper.load_model("base")
        result = model.transcribe(filename)
        text = result["text"].strip()
        print("You said:", text)
        
        # Write recognized words to audiototext.txt
        with open("audiototext.txt", "w", encoding="utf-8") as f:
            f.write(text)
        print("Transcription saved to audiototext.txt")
        
        # Generate automation code using DeepSeek API Engine
        print("\nGenerating automation code...")
        engine = DeepSeekAPIEngine()
        code = engine.generate_code()
        
        if code:
            if engine.save_code(code):
                print("\nGenerated code:")
                print("-" * 50)
                print(code)
                print("-" * 50)
            #try to exec generated code
            #try:
                #exec(automation_code.py)
            #except Exception as e:
               # print(f"Automation Code could not be executed{str(e)}")

    else:
        print(f"{filename} does not exist.")
