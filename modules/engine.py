from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

class CodeEngine:
    def __init__(self):
        """Initialize the code generation engine."""
        print("Loading model...")
        self.model_name = "WizardLM/WizardCoder-Python-7B-V1.0"
        self.tok = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            torch_dtype=torch.float16,
            device_map="auto",
            load_in_4bit=True
        )
        print("Model loaded successfully!")
        

    def generate_code(self, instruction):
        """Generate Python code based on the instruction."""
        prompt = f"""<s>[INST] Write Python code to: {instruction}
        Use pyautogui, pywinauto, and selenium for automation.
        Return only the Python code, no explanations. [/INST]"""
        
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