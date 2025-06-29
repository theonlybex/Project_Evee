from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import os


class CodeEngine:
    def __init__(self):
        """Initialize the code generation engine."""
        print("Loading model...")
        self.model_name = "codellama/CodeLlama-7b-hf"
        # Get token from environment variable instead of hardcoding
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
        print("Model loaded successfully!")
        

    def generate_code(self):

        # Instructions for the model
        instruction = """
        [/INST]You are a personal in-house POC assistant.
        Your purpose is to receive text text commands (e.g., "I want to watch some youtube videos")
        and write python code using pyautogui, pywinauto, selenium to complete the task[/INST]


        """
        # Read the user command from the text file
        user_request = open("audiototext.txt", "r").read()

        #creation of the prompt
        prompt = instruction+ "### User Command:\n" + user_request + "\n\n### Assistant Response (Python Code): \n"
        
        try:
            # Tokenize and generate
            inputs = self.tok(prompt, return_tensors="pt").to(self.model.device)
            out = self.model.generate(
                **inputs, 
                max_new_tokens=256, 
                temperature=0.1
            )
            code = self.tok.decode(out[0], skip_special_tokens=True)
            
            # Extract only the code part after the instruction
            code = code.split("[/INST]")[-1].strip()
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