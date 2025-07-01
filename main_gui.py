import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import threading
import os
import warnings
import time
import json
import math
from datetime import datetime

warnings.filterwarnings("ignore", message="FP16 is not supported on CPU")

try:
    from modules import voice_input as recording
    from modules.deepseek_api_engine import DeepSeekAPIEngine
    import whisper
except ImportError as e:
    messagebox.showerror("Import Error", f"Required modules not found: {e}\nPlease install dependencies first.")

class VoiceAutomationGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Project Evee - Voice Automation Assistant")
        self.root.geometry("900x700")
        self.root.configure(bg='#0f0f23')
        
        # Initialize variables
        self.is_recording = False
        self.whisper_model = None
        self.deepseek_engine = None
        self.current_transcription = ""
        self.generated_code = ""
        self.conversation_history = []
        self.animation_running = False
        self.circle_phase = 0
        
        # Load whisper model in background
        self.load_models()
        
        # Create GUI elements
        self.create_widgets()
        
        # Load settings
        self.load_settings()
    
    def create_widgets(self):
        # Header
        header_frame = tk.Frame(self.root, bg='#0f0f23', height=60)
        header_frame.pack(fill='x', padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        # Title in header
        title_label = tk.Label(header_frame, text="🎙️ Project Evee", 
                              font=('Segoe UI', 20, 'bold'), 
                              bg='#0f0f23', fg='#ffffff')
        title_label.pack(side='left', padx=20, pady=15)
        
        # Settings button in header
        self.settings_btn = tk.Button(header_frame, text=" ⚙️ ", 
                                     command=self.open_settings,
                                     bg='#2d2d2d', fg='#ffffff', 
                                     font=('Segoe UI', 12),
                                     bd=0, padx=10, pady=5,
                                     activebackground='#404040',
                                     cursor='hand2')
        self.settings_btn.pack(side='right', padx=20, pady=15)
        
        # Main conversation area
        self.main_frame = tk.Frame(self.root, bg='#0f0f23')
        self.main_frame.pack(fill='both', expand=True, padx=0, pady=0)
        
        # Conversation scrollable area
        self.canvas = tk.Canvas(self.main_frame, bg='#0f0f23', highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg='#0f0f23')
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # Welcome message
        self.add_assistant_message("Hi! I'm your voice automation assistant. Click the microphone and tell me what you'd like to automate. I'll listen, understand, and execute it automatically!")
        
        # Center circle area
        self.circle_frame = tk.Frame(self.main_frame, bg='#0f0f23', height=200)
        self.circle_frame.pack(side='bottom', fill='x', pady=20)
        self.circle_frame.pack_propagate(False)
        
        # Canvas for animated circle
        self.circle_canvas = tk.Canvas(self.circle_frame, bg='#0f0f23', 
                                      height=120, highlightthickness=0)
        self.circle_canvas.pack(expand=True)
        
        # Control buttons below circle
        control_frame = tk.Frame(self.root, bg='#0f0f23', height=80)
        control_frame.pack(fill='x', pady=(0, 20))
        control_frame.pack_propagate(False)
        
        # Button container
        button_container = tk.Frame(control_frame, bg='#0f0f23')
        button_container.pack(expand=True)
        
        # Record button (main action)
        self.record_btn = tk.Button(button_container, text="🎤", 
                                   command=self.toggle_recording,
                                   bg='#10a37f', fg='white', 
                                   font=('Segoe UI', 18),
                                   width=4, height=1, bd=0,
                                   activebackground='#0d8b6f',
                                   cursor='hand2')
        self.record_btn.pack(side='left', padx=10)
        
        # Secondary buttons (smaller)
        self.generate_btn = tk.Button(button_container, text="🤖", 
                                     command=self.generate_automation_code,
                                     bg='#2d2d2d', fg='white', 
                                     font=('Segoe UI', 14),
                                     width=3, height=1, bd=0,
                                     activebackground='#404040',
                                     cursor='hand2')
        self.generate_btn.pack(side='left', padx=5)
        
        self.execute_btn = tk.Button(button_container, text="▶️", 
                                    command=self.execute_generated_code,
                                    bg='#2d2d2d', fg='white', 
                                    font=('Segoe UI', 14),
                                    width=3, height=1, bd=0,
                                    activebackground='#404040',
                                    cursor='hand2')
        self.execute_btn.pack(side='left', padx=5)
        
        self.save_btn = tk.Button(button_container, text="💾", 
                                 command=self.save_code,
                                 bg='#2d2d2d', fg='white', 
                                 font=('Segoe UI', 14),
                                 width=3, height=1, bd=0,
                                 activebackground='#404040',
                                 cursor='hand2')
        self.save_btn.pack(side='left', padx=5)
        
        # Status text
        self.status_label = tk.Label(control_frame, text="Ready to listen - Speak and I'll automate it!", 
                                    font=('Segoe UI', 11), 
                                    bg='#0f0f23', fg='#8e8ea0')
        self.status_label.pack(pady=(5, 0))
        
        # Start the circle animation
        self.animate_circle()
    
    def add_user_message(self, message):
        """Add a user message to the conversation"""
        message_frame = tk.Frame(self.scrollable_frame, bg='#0f0f23')
        message_frame.pack(fill='x', padx=20, pady=(10, 5), anchor='e')
        
        # User message bubble
        bubble_frame = tk.Frame(message_frame, bg='#0f0f23')
        bubble_frame.pack(side='right')
        
        user_bubble = tk.Label(bubble_frame, text=message, 
                              bg='#10a37f', fg='white',
                              font=('Segoe UI', 11), 
                              wraplength=400, justify='left',
                              padx=15, pady=10)
        user_bubble.pack(side='right')
        
        # Auto-scroll to bottom
        self.root.after(100, lambda: self.canvas.yview_moveto(1.0))
    
    def add_assistant_message(self, message, message_type="text"):
        """Add an assistant message to the conversation"""
        message_frame = tk.Frame(self.scrollable_frame, bg='#0f0f23')
        message_frame.pack(fill='x', padx=20, pady=(5, 10), anchor='w')
        
        # Assistant avatar
        avatar_label = tk.Label(message_frame, text="🤖", 
                               font=('Segoe UI', 16), 
                               bg='#0f0f23', fg='#10a37f')
        avatar_label.pack(side='left', padx=(0, 10), pady=(0, 0))
        
        # Assistant message bubble
        bubble_frame = tk.Frame(message_frame, bg='#0f0f23')
        bubble_frame.pack(side='left', fill='x', expand=True)
        
        if message_type == "code":
            # Code block styling
            code_frame = tk.Frame(bubble_frame, bg='#1e1e1e', bd=1, relief='solid')
            code_frame.pack(fill='x', pady=5)
            
            code_label = tk.Label(code_frame, text="Generated Code:", 
                                 bg='#1e1e1e', fg='#569cd6',
                                 font=('Segoe UI', 9, 'bold'),
                                 anchor='w')
            code_label.pack(fill='x', padx=10, pady=(5, 0))
            
            code_text = tk.Text(code_frame, bg='#1e1e1e', fg='#d4d4d4',
                               font=('Consolas', 10), height=10,
                               wrap=tk.WORD, bd=0, padx=10, pady=5)
            code_text.pack(fill='x', padx=5, pady=(0, 5))
            code_text.insert('1.0', message)
            code_text.config(state='disabled')
        else:
            # Regular text message
            assistant_bubble = tk.Label(bubble_frame, text=message, 
                                       bg='#2d2d2d', fg='#ffffff',
                                       font=('Segoe UI', 11), 
                                       wraplength=450, justify='left',
                                       padx=15, pady=10, anchor='w')
            assistant_bubble.pack(side='left', fill='x')
        
        # Auto-scroll to bottom
        self.root.after(100, lambda: self.canvas.yview_moveto(1.0))
    
    def animate_circle(self):
        """Animate the central circle"""
        if not hasattr(self, 'circle_canvas'):
            return
            
        self.circle_canvas.delete("all")
        
        # Get canvas dimensions
        canvas_width = self.circle_canvas.winfo_width() or 400
        canvas_height = self.circle_canvas.winfo_height() or 120
        center_x = canvas_width // 2
        center_y = canvas_height // 2
        
        if self.is_recording:
            # Pulsing animation while recording
            base_radius = 30
            pulse = math.sin(self.circle_phase * 0.3) * 10
            radius = base_radius + pulse
            
            # Draw multiple circles for effect
            for i in range(3):
                alpha_radius = radius - (i * 8)
                if alpha_radius > 0:
                    color = f"#{hex(255-i*40)[2:].zfill(2)}4444"
                    self.circle_canvas.create_oval(
                        center_x - alpha_radius, center_y - alpha_radius,
                        center_x + alpha_radius, center_y + alpha_radius,
                        fill=color, outline="", width=0
                    )
            
            # Microphone icon
            self.circle_canvas.create_text(center_x, center_y, text="🎤", 
                                         font=('Segoe UI', 20), fill='white')
        
        elif self.animation_running:
            # Processing animation
            base_radius = 25
            for i in range(3):
                angle = (self.circle_phase + i * 120) * math.pi / 180
                x = center_x + math.cos(angle) * 15
                y = center_y + math.sin(angle) * 15
                
                self.circle_canvas.create_oval(
                    x - 8, y - 8, x + 8, y + 8,
                    fill='#10a37f', outline="", width=0
                )
        else:
            # Static idle state - ready to automate
            self.circle_canvas.create_oval(
                center_x - 25, center_y - 25,
                center_x + 25, center_y + 25,
                fill='#2d2d2d', outline='#10a37f', width=2
            )
            # Gentle pulsing to show it's ready
            pulse_factor = (math.sin(self.circle_phase * 0.1) + 1) * 0.1 + 0.8
            color_intensity = int(16 + pulse_factor * 20)
            self.circle_canvas.create_text(center_x, center_y, text="🤖", 
                                         font=('Segoe UI', 20), 
                                         fill=f'#{color_intensity:02x}a37f')
        
        self.circle_phase += 1
        self.root.after(50, self.animate_circle)
    
    def load_models(self):
        """Load AI models in a separate thread"""
        def load_in_background():
            try:
                self.update_status("Loading AI models...")
                self.animation_running = True
                self.whisper_model = whisper.load_model("base")
                
                self.update_status("Initializing AI engine...")
                self.deepseek_engine = DeepSeekAPIEngine()
                
                self.animation_running = False
                self.update_status("Ready to listen")
                self.add_assistant_message("I'm ready! Click the microphone and tell me what you'd like to automate. I'll listen, create the code, and execute it automatically!")
            except Exception as e:
                self.animation_running = False
                self.update_status("Error loading models")
                self.add_assistant_message(f"Sorry, I encountered an error loading the AI models: {str(e)}")
                messagebox.showerror("Error", f"Failed to load models: {e}")
        
        threading.Thread(target=load_in_background, daemon=True).start()
    
    def update_status(self, message):
        """Update status label from any thread"""
        self.root.after(0, lambda: self.status_label.config(text=message))
    
    def toggle_recording(self):
        """Start or stop recording"""
        if not self.is_recording:
            self.start_recording()
        else:
            self.stop_recording()
    
    def start_recording(self):
        """Start recording audio"""
        if not self.whisper_model:
            self.add_assistant_message("Please wait, I'm still loading my AI models...")
            return
        
        self.is_recording = True
        self.record_btn.config(text="🛑", bg='#dc3545')
        self.update_status("Listening... Speak clearly!")
        
        def record_audio():
            try:
                filename = "recording.wav"
                recording.record_audio(filename)
                
                if os.path.exists(filename):
                    self.update_status("Processing your voice...")
                    self.animation_running = True
                    
                    result = self.whisper_model.transcribe(filename)
                    text = result["text"].strip()
                    
                    self.current_transcription = text
                    
                    # Add user message to conversation
                    self.root.after(0, lambda: self.add_user_message(text))
                    
                    # Save to file
                    with open("audiototext.txt", "w", encoding="utf-8") as f:
                        f.write(text)
                    
                    self.animation_running = False
                    self.update_status("Got it! Creating automation...")
                    
                    # Add assistant response
                    self.root.after(0, lambda: self.add_assistant_message("I heard you say: \"" + text + "\""))
                    self.root.after(100, lambda: self.add_assistant_message("Let me create and execute the automation for you..."))
                    
                    # Automatically generate and execute code
                    self.root.after(200, self.auto_generate_and_execute)
                else:
                    self.animation_running = False
                    self.update_status("Recording failed")
                    self.add_assistant_message("Sorry, I couldn't record your voice. Please check your microphone and try again.")
                    
            except Exception as e:
                self.animation_running = False
                self.update_status("Recording error")
                self.add_assistant_message(f"I encountered an error while recording: {str(e)}")
            finally:
                self.is_recording = False
                self.root.after(0, lambda: self.record_btn.config(text="🎤", bg='#10a37f'))
        
        threading.Thread(target=record_audio, daemon=True).start()
    
    def stop_recording(self):
        """Stop recording (handled automatically by voice detection)"""
        pass
    
    def auto_generate_and_execute(self):
        """Automatically generate and execute code after voice input"""
        if not self.current_transcription:
            self.add_assistant_message("Sorry, I didn't catch what you said. Please try again.")
            return
        
        if not self.deepseek_engine:
            self.add_assistant_message("Please wait, my AI engine is still initializing...")
            return
        
        self.update_status("Creating automation code...")
        self.animation_running = True
        
        def generate_and_execute():
            try:
                # Generate code
                code = self.deepseek_engine.generate_code()
                if code:
                    self.generated_code = code
                    
                    # Show the generated code to user
                    self.root.after(0, lambda: self.add_assistant_message(code, "code"))
                    self.root.after(100, lambda: self.add_assistant_message("I've generated the automation code. Now executing it..."))
                    
                    # Short delay to show the code, then execute
                    self.root.after(1000, lambda: self.auto_execute_code())
                else:
                    self.animation_running = False
                    self.update_status("Code generation failed")
                    self.add_assistant_message("Sorry, I couldn't create automation code for that request. Please try rephrasing your command.")
                    
            except Exception as e:
                self.animation_running = False
                self.update_status("Code generation error")
                self.add_assistant_message(f"I encountered an error while generating code: {str(e)}")
        
        threading.Thread(target=generate_and_execute, daemon=True).start()
    
    def auto_execute_code(self):
        """Automatically execute the generated code"""
        if not self.generated_code:
            return
        
        self.update_status("Executing automation...")
        
        def execute_code():
            try:
                # Save code to file first
                with open("automation_code.py", "w", encoding="utf-8") as f:
                    f.write(self.generated_code)
                
                # Execute the code
                exec(self.generated_code)
                
                self.animation_running = False
                self.update_status("Ready to listen")
                self.add_assistant_message("✅ Perfect! The automation executed successfully. What would you like me to automate next?")
                
            except Exception as e:
                self.animation_running = False
                self.update_status("Ready to listen")
                error_msg = f"Execution error: {str(e)}"
                self.add_assistant_message(f"❌ I encountered an error while executing the automation:\n\n{error_msg}\n\nTry rephrasing your request or use a simpler command.")
        
        threading.Thread(target=execute_code, daemon=True).start()
    
    def generate_automation_code(self):
        """Manually generate automation code (for manual review)"""
        if not self.current_transcription:
            self.add_assistant_message("Please record a voice command first by clicking the 🎤 microphone button.")
            return
        
        if not self.deepseek_engine:
            self.add_assistant_message("Please wait, my AI engine is still initializing...")
            return
        
        self.update_status("Creating automation code...")
        self.animation_running = True
        
        self.add_assistant_message("Let me create automation code for manual review...")
        
        def generate_code():
            try:
                code = self.deepseek_engine.generate_code()
                if code:
                    self.generated_code = code
                    self.animation_running = False
                    self.update_status("Code ready! Click ▶️ to execute")
                    
                    # Add code to conversation
                    self.root.after(0, lambda: self.add_assistant_message(code, "code"))
                    self.root.after(100, lambda: self.add_assistant_message("Here's the automation code for manual review! Click ▶️ to execute, or 💾 to save it."))
                else:
                    self.animation_running = False
                    self.update_status("Code generation failed")
                    self.add_assistant_message("Sorry, I couldn't generate automation code for that request. Please try rephrasing your command.")
                    
            except Exception as e:
                self.animation_running = False
                self.update_status("Code generation error")
                self.add_assistant_message(f"I encountered an error while generating code: {str(e)}")
        
        threading.Thread(target=generate_code, daemon=True).start()
    
    def execute_generated_code(self):
        """Manually execute the generated code (with confirmation)"""
        if not self.generated_code:
            self.add_assistant_message("Please generate automation code first by clicking the 🤖 button, or simply record a new voice command for automatic execution.")
            return
        
        # Confirm execution
        result = messagebox.askyesno("Manual Execution Confirmation", 
                                   "Are you sure you want to manually execute this code?\n\n" +
                                   "This will perform automated actions on your computer.\n\n" +
                                   "Note: Voice commands are executed automatically!")
        if not result:
            self.add_assistant_message("Manual execution cancelled. You can always record a new voice command for automatic execution.")
            return
        
        self.update_status("Executing automation...")
        self.animation_running = True
        self.add_assistant_message("Manually executing the automation code...")
        
        def execute_code():
            try:
                # Save code to file first
                with open("automation_code.py", "w", encoding="utf-8") as f:
                    f.write(self.generated_code)
                
                # Execute the code
                exec(self.generated_code)
                
                self.animation_running = False
                self.update_status("Ready to listen - Speak and I'll automate it!")
                self.add_assistant_message("✅ Manual execution successful! Want to try another voice command? Just click the microphone!")
                
            except Exception as e:
                self.animation_running = False
                self.update_status("Ready to listen - Speak and I'll automate it!")
                error_msg = f"Execution error: {str(e)}"
                self.add_assistant_message(f"❌ Manual execution failed:\n\n{error_msg}\n\nTry recording a new voice command for automatic execution.")
        
        threading.Thread(target=execute_code, daemon=True).start()
    
    def save_code(self):
        """Save generated code to a file"""
        if not self.generated_code:
            self.add_assistant_message("No code to save yet. Record a voice command and I'll generate code automatically, or click 🤖 for manual generation.")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".py",
            filetypes=[("Python files", "*.py"), ("All files", "*.*")],
            title="Save Generated Automation Code"
        )
        
        if filename:
            try:
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(self.generated_code)
                self.add_assistant_message(f"💾 Code saved successfully to: {filename}\n\nYou can run this file later or modify it as needed!")
            except Exception as e:
                self.add_assistant_message(f"Failed to save code: {str(e)}")
        else:
            self.add_assistant_message("Save cancelled.")
    
    def stop_recording(self):
        """Stop recording (handled automatically by voice detection)"""
        pass
    
    def load_settings(self):
        """Load settings from file"""
        try:
            if os.path.exists("settings.json"):
                with open("settings.json", "r") as f:
                    settings = json.load(f)
                # Apply settings here if needed
        except Exception as e:
            print(f"Failed to load settings: {e}")
    
    def save_settings(self, settings):
        """Save settings to file"""
        try:
            with open("settings.json", "w") as f:
                json.dump(settings, f, indent=2)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings: {e}")
    
    def open_settings(self):
        """Open settings dialog"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings - Project Evee")
        settings_window.geometry("450x350")
        settings_window.configure(bg='#0f0f23')
        settings_window.resizable(False, False)
        
        # Header
        header_label = tk.Label(settings_window, text="⚙️ Settings", 
                               font=('Segoe UI', 18, 'bold'), 
                               bg='#0f0f23', fg='#ffffff')
        header_label.pack(pady=(20, 30))
        
        # API Key setting
        api_frame = tk.Frame(settings_window, bg='#0f0f23')
        api_frame.pack(fill='x', padx=30, pady=10)
        
        tk.Label(api_frame, text="DeepSeek API Key:", 
                bg='#0f0f23', fg='#ffffff', 
                font=('Segoe UI', 12, 'bold')).pack(anchor='w', pady=(0, 5))
        
        api_key_entry = tk.Entry(api_frame, width=50, show='*',
                                bg='#2d2d2d', fg='#ffffff', 
                                font=('Segoe UI', 10),
                                bd=1, relief='solid', insertbackground='white')
        api_key_entry.pack(fill='x', pady=(0, 5))
        
        if self.deepseek_engine:
            api_key_entry.insert(0, self.deepseek_engine.api_key)
        
        tk.Label(api_frame, text="Get your API key from: https://platform.deepseek.com/", 
                bg='#0f0f23', fg='#8e8ea0', 
                font=('Segoe UI', 9)).pack(anchor='w')
        
        # Recording settings
        record_frame = tk.Frame(settings_window, bg='#0f0f23')
        record_frame.pack(fill='x', padx=30, pady=20)
        
        tk.Label(record_frame, text="Recording Settings:", 
                bg='#0f0f23', fg='#ffffff', 
                font=('Segoe UI', 12, 'bold')).pack(anchor='w', pady=(0, 10))
        
        timeout_frame = tk.Frame(record_frame, bg='#0f0f23')
        timeout_frame.pack(fill='x')
        
        tk.Label(timeout_frame, text="Silence Timeout:", 
                bg='#0f0f23', fg='#ffffff', 
                font=('Segoe UI', 10)).pack(side='left')
        
        timeout_var = tk.StringVar(value="4")
        timeout_entry = tk.Entry(timeout_frame, textvariable=timeout_var, width=5,
                                bg='#2d2d2d', fg='#ffffff', 
                                font=('Segoe UI', 10),
                                bd=1, relief='solid', insertbackground='white')
        timeout_entry.pack(side='left', padx=(10, 5))
        
        tk.Label(timeout_frame, text="seconds", 
                bg='#0f0f23', fg='#8e8ea0', 
                font=('Segoe UI', 10)).pack(side='left')
        
        # Button frame
        button_frame = tk.Frame(settings_window, bg='#0f0f23')
        button_frame.pack(fill='x', padx=30, pady=30)
        
        # Save button
        def save_settings():
            new_api_key = api_key_entry.get()
            if new_api_key and self.deepseek_engine:
                self.deepseek_engine.api_key = new_api_key
                self.deepseek_engine.headers["Authorization"] = f"Bearer {new_api_key}"
            
            settings = {
                "api_key": new_api_key,
                "silence_timeout": timeout_var.get()
            }
            self.save_settings(settings)
            self.add_assistant_message("Settings saved successfully! 🎉")
            settings_window.destroy()
        
        # Cancel button
        cancel_btn = tk.Button(button_frame, text="Cancel", 
                             command=settings_window.destroy,
                             bg='#2d2d2d', fg='#ffffff', 
                             font=('Segoe UI', 10),
                             bd=0, padx=20, pady=8,
                             activebackground='#404040',
                             cursor='hand2')
        cancel_btn.pack(side='right', padx=(10, 0))
        
        save_btn = tk.Button(button_frame, text="Save Settings", 
                           command=save_settings,
                           bg='#10a37f', fg='#ffffff', 
                           font=('Segoe UI', 10, 'bold'),
                           bd=0, padx=20, pady=8,
                           activebackground='#0d8b6f',
                           cursor='hand2')
        save_btn.pack(side='right')

def main():
    root = tk.Tk()
    app = VoiceAutomationGUI(root)
    
    # Handle window closing
    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    main() 