import os
import warnings
import whisper

warnings.filterwarnings("ignore", message="FP16 is not supported on CPU")

class WhisperEngine:
    """
    A class to handle speech transcription using OpenAI's Whisper model.
    
    Supports different model sizes and provides clean transcription functionality
    with error handling and file management.
    """
    
    def __init__(self, model_size="base"):
        """
        Initialize the WhisperEngine.
        
        Args:
            model_size (str): Size of the Whisper model to use.
                            Options: "tiny", "base", "small", "medium", "large"
                            Default: "base" (good balance of speed vs accuracy)
        """
        self.model_size = model_size
        self.model = None
        self.is_loaded = False
        
        # Supported model sizes with their characteristics
        self.model_info = {
            "tiny": {"params": "39M", "speed": "~32x", "use_case": "Very fast, basic accuracy"},
            "base": {"params": "74M", "speed": "~16x", "use_case": "Good balance (recommended)"},
            "small": {"params": "244M", "speed": "~6x", "use_case": "Better accuracy, slower"},
            "medium": {"params": "769M", "speed": "~2x", "use_case": "High accuracy, much slower"},
            "large": {"params": "1550M", "speed": "1x", "use_case": "Best accuracy, slowest"}
        }
    
    def load_model(self):
        """
        Load the Whisper model.
        
        Returns:
            bool: True if model loaded successfully, False otherwise
        """
        if self.is_loaded:
            print(f"✅ Whisper model '{self.model_size}' already loaded")
            return True
        
        try:
            print(f"🔄 Loading Whisper model '{self.model_size}'...")
            
            if self.model_size not in self.model_info:
                available = ", ".join(self.model_info.keys())
                raise ValueError(f"Invalid model size '{self.model_size}'. Available: {available}")
            
            self.model = whisper.load_model(self.model_size)
            self.is_loaded = True
            
            info = self.model_info[self.model_size]
            print(f"✅ Whisper model '{self.model_size}' loaded successfully!")
            print(f"   📊 Parameters: {info['params']}, Speed: {info['speed']}")
            print(f"   💡 Use case: {info['use_case']}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error loading Whisper model: {e}")
            self.model = None
            self.is_loaded = False
            return False
    
    def transcribe_file(self, audio_file_path, language=None, save_to_file=True):
        """
        Transcribe an audio file to text.
        
        Args:
            audio_file_path (str): Path to the audio file
            language (str, optional): Language code (e.g., "en", "es", "fr").
                                    If None, Whisper will auto-detect
            save_to_file (bool): Whether to save transcription to audiototext.txt
            
        Returns:
            dict: Transcription result with 'text', 'segments', and 'language'
                 Returns None if transcription fails
        """
        if not self.is_loaded:
            print("❌ Model not loaded. Call load_model() first.")
            return None
        
        if not os.path.exists(audio_file_path):
            print(f"❌ Audio file not found: {audio_file_path}")
            return None
        
        try:
            print(f"🔄 Transcribing: {os.path.basename(audio_file_path)}")
            
            # Prepare transcription options
            options = {}
            if language:
                options["language"] = language
                print(f"   🌐 Language set to: {language}")
            else:
                print("   🔍 Auto-detecting language...")
            
            # Perform transcription
            result = self.model.transcribe(audio_file_path, **options)
            
            # Extract information
            transcription_text = result["text"].strip()
            detected_language = result.get("language", "unknown")
            
            print(f"✅ Transcription completed!")
            print(f"   🌐 Detected language: {detected_language}")
            print(f"   📝 Text length: {len(transcription_text)} characters")
            
            # Save to file if requested
            if save_to_file and transcription_text:
                self.save_transcription(transcription_text)
            
            return {
                "text": transcription_text,
                "segments": result.get("segments", []),
                "language": detected_language,
                "audio_file": audio_file_path
            }
            
        except Exception as e:
            print(f"❌ Transcription error: {e}")
            return None
    
    def save_transcription(self, text, filename="audiototext.txt"):
        """
        Save transcription text to a file.
        
        Args:
            text (str): Transcription text to save
            filename (str): Name of the file to save to
            
        Returns:
            bool: True if saved successfully, False otherwise
        """
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(text)
            print(f"💾 Transcription saved to: {filename}")
            return True
        except Exception as e:
            print(f"❌ Error saving transcription: {e}")
            return False
    
    def get_model_info(self):
        """
        Get information about available models and current model.
        
        Returns:
            dict: Model information
        """
        return {
            "current_model": self.model_size,
            "is_loaded": self.is_loaded,
            "available_models": self.model_info
        }
    
    def change_model(self, new_model_size):
        """
        Change to a different Whisper model size.
        
        Args:
            new_model_size (str): New model size to load
            
        Returns:
            bool: True if model changed successfully
        """
        if new_model_size == self.model_size and self.is_loaded:
            print(f"✅ Already using model '{new_model_size}'")
            return True
        
        print(f"🔄 Changing from '{self.model_size}' to '{new_model_size}'...")
        
        # Reset current model
        self.model = None
        self.is_loaded = False
        self.model_size = new_model_size
        
        # Load new model
        return self.load_model()
    
    def __str__(self):
        status = "loaded" if self.is_loaded else "not loaded"
        return f"WhisperEngine(model='{self.model_size}', status='{status}')" 