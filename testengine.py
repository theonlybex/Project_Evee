from transformers import AutoTokenizer, AutoModelForCasualLM
import torch

# Load the model and tokenizer
model_name = "zuozishi/wizardcoder-7b-instruct"

tok = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCasualLM.from_pretrained(
    model_name,
    load_in_4bit=True,
    device_map="auto"
)

# Instructions for the model
instruction_prefix = """
You are a personal in-house POC assistant.
Your purpose is to receive text text commands (e.g., "I want to watch some youtube videos")
and write python code using pyautogui, pywinauto, selenium to complete the task


"""
# Read the user command from the text file
user_request = open("audiototext.txt", "r").read()

#creation of the prompt
prompt = instruction_prefix + "### User Command:\n" + user_request + "\n\n### Assistant Response (Python Code): \n"

# generate the code
inputs = tok(prompt, return_tensors="pt").to(model.device)
out = model.generate(**inputs, max_new_tokens=256, temperature=0.1)
code = tok.decode(out[0], skip_special_tokens=True)

# Save the code to a file
filename = "GUI.py"
with open(filename, "w", encoding="utf-8") as f:
    f.write(code)

print("Python code generated and saved to codeGen.py")
