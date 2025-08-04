import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import threading
import os
import warnings
import time
import json
from datetime import datetime

warnings.filterwarnings("ignore", message="FP16 is not supported on CPU")

try:
    from modules import voice_input as recording
    from modules.openai_engine import OpenAICodeEngine
    from modules.file_manager import get_file_manager
    import whisper
except ImportError as e:
    messagebox.showerror("Import Error", f"Required modules not found: {e}\nPlease install dependencies first.")

class VoiceAutomationGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Project Evee - Voice Automation Assistant")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')
        
        # Initialize variables
        self.is_recording = False
        self.whisper_model = None
        self.openai_engine = None
        self.current_transcription = ""
        self.generated_code = ""
        
        # Initialize file manager
        self.file_manager = get_file_manager()
        
        # Load whisper model in background
        self.load_models()
        
        # Create GUI elements
        self.create_widgets()
        
        # Load settings
        self.load_settings()
    
    def create_widgets(self):
        # Title
        title_frame = tk.Frame(self.root, bg='#f0f0f0')
        title_frame.pack(fill='x', padx=20, pady=10)
        
        title_label = tk.Label(title_frame, text="🎙️ Project Evee", 
                              font=('Arial', 24, 'bold'), 
                              bg='#f0f0f0', fg='#333')
        title_label.pack()
        
        subtitle_label = tk.Label(title_frame, text="Voice-Controlled Automation Assistant", 
                                 font=('Arial', 12), 
                                 bg='#f0f0f0', fg='#666')
        subtitle_label.pack()
        
        # Main container
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Left panel - Controls
        left_frame = tk.LabelFrame(main_frame, text="Controls", 
                                  font=('Arial', 12, 'bold'), 
                                  bg='#f0f0f0', fg='#333')
        left_frame.pack(side='left', fill='y', padx=(0, 10))
        
        # Record button
        self.record_btn = tk.Button(left_frame, text="🎤 Start Recording", 
                                   command=self.toggle_recording,
                                   bg='#4CAF50', fg='white', 
                                   font=('Arial', 12, 'bold'),
                                   width=15, height=2)
        self.record_btn.pack(pady=10)
        
        # Status label
        self.status_label = tk.Label(left_frame, text="Ready", 
                                    font=('Arial', 10), 
                                    bg='#f0f0f0', fg='#333')
        self.status_label.pack(pady=5)
        
        # Progress bar
        self.progress = ttk.Progressbar(left_frame, mode='indeterminate')
        self.progress.pack(fill='x', padx=10, pady=5)
        
        # Note: Execute Command button removed - now happens automatically after voice recording
        # The workflow is now: Record Voice → Transcribe → Auto-Execute (with confirmation)
        
        # Save Code button
        self.save_btn = tk.Button(left_frame, text="💾 Save Code", 
                                 command=self.save_code,
                                 bg='#9C27B0', fg='white', 
                                 font=('Arial', 12, 'bold'),
                                 width=15, height=2)
        self.save_btn.pack(pady=10)
        
        # Settings button
        self.settings_btn = tk.Button(left_frame, text="⚙️ Settings", 
                                     command=self.open_settings,
                                     bg='#607D8B', fg='white', 
                                     font=('Arial', 12, 'bold'),
                                     width=15, height=2)
        self.settings_btn.pack(pady=10)
        
        # Right panel - Output
        right_frame = tk.Frame(main_frame, bg='#f0f0f0')
        right_frame.pack(side='right', fill='both', expand=True)
        
        # Notebook for tabs
        self.notebook = ttk.Notebook(right_frame)
        self.notebook.pack(fill='both', expand=True)
        
        # Transcription tab
        transcription_frame = tk.Frame(self.notebook, bg='white')
        self.notebook.add(transcription_frame, text="📝 Transcription")
        
        self.transcription_text = scrolledtext.ScrolledText(transcription_frame, 
                                                           wrap=tk.WORD, 
                                                           font=('Consolas', 11))
        self.transcription_text.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Generated Code tab
        code_frame = tk.Frame(self.notebook, bg='white')
        self.notebook.add(code_frame, text="💻 Generated Code")
        
        self.code_text = scrolledtext.ScrolledText(code_frame, 
                                                  wrap=tk.WORD, 
                                                  font=('Consolas', 11))
        self.code_text.pack(fill='both', expand=True, padx=10, pady=10)
        
        # History tab
        history_frame = tk.Frame(self.notebook, bg='white')
        self.notebook.add(history_frame, text="📊 History")
        
        self.history_text = scrolledtext.ScrolledText(history_frame, 
                                                     wrap=tk.WORD, 
                                                     font=('Consolas', 10))
        self.history_text.pack(fill='both', expand=True, padx=10, pady=10)
    
    def load_models(self):
        """Load AI models in a separate thread"""
        def load_in_background():
            try:
                self.update_status("Loading Whisper model...")
                self.progress.start()
                self.whisper_model = whisper.load_model("base")
                
                self.update_status("Initializing OpenAI engine...")
                self.openai_engine = OpenAICodeEngine()
                
                self.progress.stop()
                self.update_status("Ready")
            except Exception as e:
                self.progress.stop()
                self.update_status("Error loading models")
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
            messagebox.showwarning("Warning", "Models are still loading. Please wait...")
            return
        
        self.is_recording = True
        self.record_btn.config(text="🛑 Stop Recording", bg='#f44336')
        self.update_status("Recording... Speak now!")
        self.progress.start()
        
        def record_audio():
            try:
                filename = "recording.wav"
                recording.record_audio(filename)
                
                if os.path.exists(filename):
                    self.update_status("Transcribing audio...")
                    result = self.whisper_model.transcribe(filename)
                    text = result["text"].strip()
                    
                    self.current_transcription = text
                    self.root.after(0, self.display_transcription)
                    
                    # Save to file using file manager
                    self.file_manager.save_transcription(text)
                    
                    self.add_to_history(f"Transcription: {text}")
                    self.update_status("Transcription complete")
                    
                    # Automatically execute the command after transcription
                    self.root.after(1000, self.generate_automation_code)  # Small delay to show transcription
                else:
                    self.update_status("Recording failed")
                    messagebox.showerror("Error", "Recording failed!")
                    
            except Exception as e:
                self.update_status("Recording error")
                messagebox.showerror("Error", f"Recording error: {e}")
            finally:
                self.progress.stop()
                self.is_recording = False
                self.root.after(0, lambda: self.record_btn.config(text="🎤 Start Recording", bg='#4CAF50'))
        
        threading.Thread(target=record_audio, daemon=True).start()
    
    def stop_recording(self):
        """Stop recording (handled automatically by voice detection)"""
        pass
    
    def display_transcription(self):
        """Display transcription in the text widget"""
        self.transcription_text.delete(1.0, tk.END)
        self.transcription_text.insert(1.0, self.current_transcription)
        self.notebook.select(0)  # Switch to transcription tab
    
    def generate_automation_code(self):
        """Generate and execute automation code with confirmation"""
        if not self.current_transcription:
            messagebox.showwarning("Warning", "No transcription available. Please record audio first.")
            return
        
        if not self.openai_engine:
            messagebox.showwarning("Warning", "OpenAI engine not initialized. Please wait...")
            return
        
        # Show confirmation dialog
        result = messagebox.askyesno(
            "Confirm Command", 
            f'Execute: "{self.current_transcription}"?',
            icon='question'
        )
        
        if not result:
            self.update_status("Command cancelled.")
            return
        
        self.update_status(f"Executing Command: {self.current_transcription}")
        self.progress.start()
        
        def generate_and_execute():
            try:
                # Generate code
                code = self.openai_engine.generate_code()
                if code:
                    self.generated_code = code
                    
                    # Save code to file using file manager
                    self.file_manager.save_automation_code(code)
                    
                    # Execute immediately
                    exec(code)
                    
                    self.root.after(0, lambda: self.display_generated_code())
                    self.add_to_history(f"Executed: {self.current_transcription}")
                    self.root.after(0, lambda: self.update_status("✅ Command executed successfully!"))
                else:
                    self.root.after(0, lambda: self.update_status("❌ Could not generate automation for this command."))
                    
            except Exception as e:
                error_msg = f"❌ Command failed: {str(e)}"
                self.root.after(0, lambda: self.update_status(error_msg))
            finally:
                self.root.after(0, lambda: self.progress.stop())
        
        threading.Thread(target=generate_and_execute, daemon=True).start()
    
    def display_generated_code(self):
        """Display generated code in the text widget"""
        self.code_text.delete(1.0, tk.END)
        self.code_text.insert(1.0, self.generated_code)
        self.notebook.select(1)  # Switch to code tab
    
    # Note: execute_generated_code method removed - 
    # Execution now happens automatically after confirmation in generate_automation_code()
    
    def save_code(self):
        """Save generated code to a file"""
        if not self.generated_code:
            messagebox.showwarning("Warning", "No code generated yet.")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".py",
            filetypes=[("Python files", "*.py"), ("All files", "*.*")],
            title="Save Generated Code"
        )
        
        if filename:
            try:
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(self.generated_code)
                self.add_to_history(f"Saved code to: {filename}")
                messagebox.showinfo("Success", f"Code saved to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save code: {e}")
    
    def add_to_history(self, entry):
        """Add entry to history"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        history_entry = f"[{timestamp}] {entry}\n"
        self.history_text.insert(tk.END, history_entry)
        self.history_text.see(tk.END)
    
    def load_settings(self):
        """Load settings from file"""
        try:
            settings = self.file_manager.load_settings()
            # Apply settings here if needed
            return settings
        except Exception as e:
            print(f"Failed to load settings: {e}")
            return {}
    
    def save_settings(self, settings):
        """Save settings to file"""
        if self.file_manager.save_settings(settings):
            return True
        else:
            messagebox.showerror("Error", "Failed to save settings")
            return False
    
    def open_settings(self):
        """Open settings dialog"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings")
        settings_window.geometry("400x300")
        settings_window.configure(bg='#f0f0f0')
        
        # API Key setting
        api_frame = tk.LabelFrame(settings_window, text="OpenAI API Settings", 
                                 font=('Arial', 12, 'bold'), bg='#f0f0f0')
        api_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(api_frame, text="API Key:", bg='#f0f0f0').pack(anchor='w', padx=10, pady=5)
        api_key_entry = tk.Entry(api_frame, width=50, show='*')
        api_key_entry.pack(fill='x', padx=10, pady=5)
        
        if self.openai_engine:
            api_key_entry.insert(0, self.openai_engine.api_key)
        
        # Recording settings
        record_frame = tk.LabelFrame(settings_window, text="Recording Settings", 
                                   font=('Arial', 12, 'bold'), bg='#f0f0f0')
        record_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(record_frame, text="Silence Timeout (seconds):", bg='#f0f0f0').pack(anchor='w', padx=10, pady=5)
        timeout_var = tk.StringVar(value="4")
        timeout_entry = tk.Entry(record_frame, textvariable=timeout_var)
        timeout_entry.pack(fill='x', padx=10, pady=5)
        
        # Save button
        def save_settings():
            new_api_key = api_key_entry.get()
            if new_api_key and self.openai_engine:
                self.openai_engine.api_key = new_api_key
                # Reinitialize OpenAI client with new API key
                from openai import OpenAI
                self.openai_engine.client = OpenAI(api_key=new_api_key)
            
            settings = {
                "openai_api_key": new_api_key,
                "silence_timeout": timeout_var.get()
            }
            if self.save_settings(settings):
                messagebox.showinfo("Success", "Settings saved!")
                settings_window.destroy()
            else:
                messagebox.showerror("Error", "Failed to save settings!")
        
        save_btn = tk.Button(settings_window, text="Save Settings", 
                           command=save_settings,
                           bg='#4CAF50', fg='white', 
                           font=('Arial', 12, 'bold'))
        save_btn.pack(pady=20)

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