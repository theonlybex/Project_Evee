from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import os


class DeepSeekEngine:
    def __init__(self):
        """Initialize the DeepSeek code generation engine."""
        print("Loading DeepSeek model...")
        self.model_name = "deepseek-ai/deepseek-coder-6.7b-base"
        self.token = os.getenv('HF_TOKEN')
        if not self.token:
            raise ValueError("Please set your Hugging Face token as an environment variable named 'HF_TOKEN'")
            
        self.tok = AutoTokenizer.from_pretrained(self.model_name, token=self.token)
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            torch_dtype=torch.float16,
            device_map="auto",
            load_in_4bit=True,
            token=self.token
        )
        print("DeepSeek model loaded successfully!")

    def generate_code(self):
        """Generate code based on the user's request."""
        # Instructions for the model
        instruction = """You are a personal in-house POC assistant.
        Your purpose is to receive text commands (e.g., "I want to watch some youtube videos")
        and write python code using pyautogui, pywinauto, selenium to complete the task.
        Only return the Python code, no explanations or markdown formatting."""

        # Read the user command from the text file
        try:
            with open("audiototext.txt", "r") as f:
                user_request = f.read()
        except FileNotFoundError:
            print("Error: audiototext.txt file not found")
            return None

        # Create the prompt
        prompt = f"{instruction}\n\nUser Command: {user_request}\n\nPython Code:"

        try:
            # Tokenize and generate
            inputs = self.tok(prompt, return_tensors="pt").to(self.model.device)
            out = self.model.generate(
                **inputs,
                max_new_tokens=512,
                temperature=0.1,
                top_p=0.95,
                do_sample=True
            )
            code = self.tok.decode(out[0], skip_special_tokens=True)
            
            # Extract only the code part after the instruction
            code = code.split("Python Code:")[-1].strip()
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