import os
import warnings
import threading
import time
import asyncio
from modules.whisper_engine import WhisperEngine
from modules.browser_use_engine import Engine
from modules import voice_input as recording
from modules.file_manager import get_file_manager

warnings.filterwarnings("ignore", message="FP16 is not supported on CPU")

async def main():
    # Initialize file manager
    file_manager = get_file_manager()
    
    whisper_obj = WhisperEngine("base")
    whisper_obj.load_model()
    engine_obj = Engine()
    print("What would you like me to do?")
    print("--------------------------------")
    print("Press 'y' to start recording")
    print("Press 'e' to execute the command")
    print("Press 'q' to quit")
    print("--------------------------------")

    while True:
        user_input = input("Enter your command:")
        if user_input == "y":
            print("Recording...")
            recording.record_audio("audio.wav")
            result = whisper_obj.transcribe_file("audio.wav")
            print("Recording stopped")
            if result:
                print(f"You asked the following: {result['text']}")
                file_manager.save_transcription(result['text'])
        elif user_input == "e":
            print("Stopping recording...")
            print("--------------------------------")
            print("Executing command...")
            print("--------------------------------")
            await engine_obj.executeCommand()
            print("Saving results...")
            engine_obj.save_results(result)
            print("--------------------------------")
            print("Command executed")
            print("--------------------------------")
            print("Final result:")
            print(result.final_result())
            break
        elif user_input == "q":
            print("Quitting...")
            break

    

if __name__ == "__main__":
    asyncio.run(main()) 