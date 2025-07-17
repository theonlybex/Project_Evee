import os
from openai import OpenAI
from .file_manager import get_file_manager


class OpenAICodeEngine:
    def __init__(self):
        """Initialize the OpenAI code generation engine."""
        print("Initializing OpenAI engine...")
        
        # Initialize file manager
        self.file_manager = get_file_manager()
        
        # Get API key from environment variable or settings
        self.api_key = os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            settings = self.file_manager.load_settings()
            self.api_key = settings.get("openai_api_key", "")
        
        if not self.api_key:
            raise ValueError("Please set your OpenAI API key in settings or as environment variable 'OPENAI_API_KEY'")
        
        self.client = OpenAI(api_key=self.api_key)
        print("OpenAI engine initialized successfully!")

    def generate_code(self):
        """Generate code based on the user's request."""
        # Instructions for the model
        instruction = """You are a personal in-house POC assistant.
        Your purpose is to receive text commands (e.g., "I want to watch some youtube videos")
        and write python code using pyautogui, pywinauto, selenium to complete the task.
        Only return the Python code, no explanations or markdown formatting."""

        # Read the user command from the file manager
        user_request = self.file_manager.load_transcription()
        if not user_request:
            print("Error: No transcription available. Please record audio first.")
            return None

        # Create the prompt
        prompt = f"{instruction}\n\nUser Command: {user_request}\n\nPython Code:"

        try:
            # Generate code using OpenAI
            response = self.client.chat.completions.create(
                model="gpt-4",  # You can also use "gpt-3.5-turbo" for a cheaper option
                messages=[
                    {"role": "system", "content": instruction},
                    {"role": "user", "content": user_request}
                ],
                temperature=0.1,  # Lower temperature for more focused code generation
                max_tokens=1000
            )
            
            # Extract the generated code
            code = response.choices[0].message.content.strip()
            return code
            
        except Exception as e:
            print(f"Error generating code: {str(e)}")
            return None

    def save_code(self, code, filename="automation_code.py"):
        """Save the generated code to a file."""
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(code)
            print(f"Code saved to {filename}")
            return True
        except Exception as e:
            print(f"Error saving code: {str(e)}")
            return False 