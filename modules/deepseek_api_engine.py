import os
import requests
import json
import re
from .file_manager import get_file_manager


class DeepSeekAPIEngine:
    def __init__(self):
        """Initialize the DeepSeek API engine."""
        print("Initializing DeepSeek API engine...")
        
        # Initialize file manager
        self.file_manager = get_file_manager()
        
        # Load API key from settings
        settings = self.file_manager.load_settings()
        self.api_key = settings.get("api_key", "sk-49d740ae018f48f7812efa9af1bbd981")
        
        self.api_url = "https://api.deepseek.com/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        print("DeepSeek API engine initialized successfully!")

    def clean_code(self, text):
        """Clean the response to extract only Python code."""
        # Remove markdown code block markers
        text = re.sub(r'```python\s*', '', text)
        text = re.sub(r'```\s*$', '', text)
        
        # Remove any leading/trailing whitespace
        text = text.strip()
        
        return text

    def generate_code(self):
        """Generate code based on the user's request."""
        # Instructions for the model
        instruction = """You are a personal in-house POC assistant.
        Your purpose is to receive text commands (e.g., "I want to watch some youtube videos")
        and write python code using pyautogui, pywinauto, selenium to complete the task.
        Return ONLY the Python code, no explanations, no markdown formatting, no comments, no text before or after the code."""

        # Read the user command from the file manager
        user_request = self.file_manager.load_transcription()
        if not user_request:
            print("Error: No transcription available. Please record audio first.")
            return None

        # Prepare the API request
        payload = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": instruction},
                {"role": "user", "content": user_request}
            ],
            "temperature": 0.1,
            "max_tokens": 1000
        }

        try:
            # Make the API request
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=payload
            )
            response.raise_for_status()  # Raise an exception for bad status codes
            
            # Parse the response
            result = response.json()
            code = result['choices'][0]['message']['content'].strip()
            
            # Clean the code
            code = self.clean_code(code)
            return code
            
        except requests.exceptions.RequestException as e:
            print(f"Error making API request: {str(e)}")
            return None
        except (KeyError, json.JSONDecodeError) as e:
            print(f"Error parsing API response: {str(e)}")
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