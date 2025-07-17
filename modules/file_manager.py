#!/usr/bin/env python3
"""
Project Evee - File Manager
Handles all file operations with absolute paths and proper error handling.
"""

import os
import json
import threading
from pathlib import Path
from typing import Optional, Dict, Any


class FileManager:
    """Manages file operations for Project Evee with absolute paths and error handling."""
    
    def __init__(self):
        """Initialize the file manager with project root directory."""
        # Get the absolute path to the project root (where this script is located)
        self.project_root = Path(__file__).parent.parent.absolute()
        
        # Define file paths
        self.files = {
            'transcription': self.project_root / 'audiototext.txt',
            'audio_recording': self.project_root / 'recording.wav',
            'automation_code': self.project_root / 'automation_code.py',
            'settings': self.project_root / 'settings.json',
            'results': self.project_root / 'results.json',
            'history': self.project_root / 'history.log'
        }
        
        # Thread lock for file operations
        self._lock = threading.Lock()
        
        # Ensure project directory exists
        self.project_root.mkdir(exist_ok=True)
        
        # Initialize essential files
        self._initialize_files()
    
    def _initialize_files(self):
        """Initialize essential files if they don't exist."""
        try:
            # Create empty transcription file if it doesn't exist
            if not self.files['transcription'].exists():
                self.save_transcription("")
            
            # Create default settings if they don't exist
            if not self.files['settings'].exists():
                self.save_settings({
                    "api_key": "",
                    "silence_timeout": 4,
                    "whisper_model": "base",
                    "auto_execute": True
                })
                
            print(f"✅ File manager initialized. Project root: {self.project_root}")
        except Exception as e:
            print(f"⚠️ Warning: Could not initialize some files: {e}")
    
    def get_project_root(self) -> Path:
        """Get the absolute path to the project root directory."""
        return self.project_root
    
    def get_file_path(self, file_type: str) -> Path:
        """Get the absolute path for a specific file type."""
        if file_type not in self.files:
            raise ValueError(f"Unknown file type: {file_type}. Available: {list(self.files.keys())}")
        return self.files[file_type]
    
    def save_transcription(self, text: str) -> bool:
        """
        Save transcription text to file safely.
        
        Args:
            text: The transcription text to save
            
        Returns:
            bool: True if successful, False otherwise
        """
        with self._lock:
            try:
                with open(self.files['transcription'], 'w', encoding='utf-8') as f:
                    f.write(text.strip())
                print(f"✅ Transcription saved: {len(text)} characters")
                return True
            except Exception as e:
                print(f"❌ Error saving transcription: {e}")
                return False
    
    def load_transcription(self, default_text: str = "") -> str:
        """
        Load transcription text from file safely.
        
        Args:
            default_text: Text to return if file doesn't exist or is empty
            
        Returns:
            str: The transcription text or default_text
        """
        with self._lock:
            try:
                if self.files['transcription'].exists():
                    with open(self.files['transcription'], 'r', encoding='utf-8') as f:
                        text = f.read().strip()
                    
                    if text:
                        return text
                    else:
                        print("⚠️ Transcription file is empty")
                        return default_text
                else:
                    print("⚠️ Transcription file not found, creating empty file")
                    self.save_transcription(default_text)
                    return default_text
                    
            except Exception as e:
                print(f"❌ Error loading transcription: {e}")
                return default_text
    
    def save_automation_code(self, code: str) -> bool:
        """
        Save automation code to file safely.
        
        Args:
            code: The Python code to save
            
        Returns:
            bool: True if successful, False otherwise
        """
        with self._lock:
            try:
                with open(self.files['automation_code'], 'w', encoding='utf-8') as f:
                    f.write(code)
                print(f"✅ Automation code saved: {len(code)} characters")
                return True
            except Exception as e:
                print(f"❌ Error saving automation code: {e}")
                return False
    
    def load_automation_code(self) -> Optional[str]:
        """
        Load automation code from file safely.
        
        Returns:
            str: The automation code or None if not found
        """
        with self._lock:
            try:
                if self.files['automation_code'].exists():
                    with open(self.files['automation_code'], 'r', encoding='utf-8') as f:
                        return f.read()
                return None
            except Exception as e:
                print(f"❌ Error loading automation code: {e}")
                return None
    
    def save_settings(self, settings: Dict[str, Any]) -> bool:
        """
        Save settings to JSON file safely.
        
        Args:
            settings: Dictionary of settings to save
            
        Returns:
            bool: True if successful, False otherwise
        """
        with self._lock:
            try:
                with open(self.files['settings'], 'w', encoding='utf-8') as f:
                    json.dump(settings, f, indent=2, ensure_ascii=False)
                print("✅ Settings saved")
                return True
            except Exception as e:
                print(f"❌ Error saving settings: {e}")
                return False
    
    def load_settings(self) -> Dict[str, Any]:
        """
        Load settings from JSON file safely.
        
        Returns:
            dict: The settings dictionary or default settings
        """
        default_settings = {
            "api_key": "",
            "silence_timeout": 4,
            "whisper_model": "base",
            "auto_execute": True
        }
        
        with self._lock:
            try:
                if self.files['settings'].exists():
                    with open(self.files['settings'], 'r', encoding='utf-8') as f:
                        settings = json.load(f)
                    # Merge with defaults to ensure all keys exist
                    return {**default_settings, **settings}
                else:
                    print("⚠️ Settings file not found, using defaults")
                    return default_settings
            except Exception as e:
                print(f"❌ Error loading settings: {e}")
                return default_settings
    
    def save_results(self, results: Dict[str, Any]) -> bool:
        """
        Save execution results to JSON file safely.
        
        Args:
            results: Dictionary of results to save
            
        Returns:
            bool: True if successful, False otherwise
        """
        with self._lock:
            try:
                with open(self.files['results'], 'w', encoding='utf-8') as f:
                    json.dump(results, f, indent=2, ensure_ascii=False)
                print("✅ Results saved")
                return True
            except Exception as e:
                print(f"❌ Error saving results: {e}")
                return False
    
    def load_results(self) -> Optional[Dict[str, Any]]:
        """
        Load execution results from JSON file safely.
        
        Returns:
            dict: The results dictionary or None if not found
        """
        with self._lock:
            try:
                if self.files['results'].exists():
                    with open(self.files['results'], 'r', encoding='utf-8') as f:
                        return json.load(f)
                return None
            except Exception as e:
                print(f"❌ Error loading results: {e}")
                return None
    
    def add_to_history(self, entry: str) -> bool:
        """
        Add an entry to the history log safely.
        
        Args:
            entry: The history entry to add
            
        Returns:
            bool: True if successful, False otherwise
        """
        with self._lock:
            try:
                from datetime import datetime
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                log_entry = f"[{timestamp}] {entry}\n"
                
                with open(self.files['history'], 'a', encoding='utf-8') as f:
                    f.write(log_entry)
                return True
            except Exception as e:
                print(f"❌ Error adding to history: {e}")
                return False
    
    def get_recent_history(self, lines: int = 50) -> list:
        """
        Get recent history entries.
        
        Args:
            lines: Number of recent lines to return
            
        Returns:
            list: List of recent history entries
        """
        try:
            if self.files['history'].exists():
                with open(self.files['history'], 'r', encoding='utf-8') as f:
                    all_lines = f.readlines()
                return all_lines[-lines:] if len(all_lines) > lines else all_lines
            return []
        except Exception as e:
            print(f"❌ Error reading history: {e}")
            return []
    
    def cleanup_temp_files(self) -> bool:
        """
        Clean up temporary files (audio recordings, etc.).
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            temp_files = [
                self.files['audio_recording'],
                self.project_root / 'audio.wav'  # backup audio file
            ]
            
            cleaned = 0
            for temp_file in temp_files:
                if temp_file.exists():
                    temp_file.unlink()
                    cleaned += 1
            
            if cleaned > 0:
                print(f"✅ Cleaned up {cleaned} temporary files")
            return True
        except Exception as e:
            print(f"❌ Error cleaning up temp files: {e}")
            return False
    
    def validate_file_integrity(self) -> Dict[str, bool]:
        """
        Validate the integrity of all managed files.
        
        Returns:
            dict: Status of each file (True = OK, False = Problem)
        """
        status = {}
        
        try:
            # Check if transcription file exists and is readable
            status['transcription'] = self.files['transcription'].exists()
            if status['transcription']:
                try:
                    self.load_transcription()
                except Exception:
                    status['transcription'] = False
            
            # Check settings file
            status['settings'] = self.files['settings'].exists()
            if status['settings']:
                try:
                    self.load_settings()
                except Exception:
                    status['settings'] = False
            
            # Check if project directory is writable
            test_file = self.project_root / '.write_test'
            try:
                test_file.write_text('test')
                test_file.unlink()
                status['writable'] = True
            except Exception:
                status['writable'] = False
            
            return status
        except Exception as e:
            print(f"❌ Error validating files: {e}")
            return {'error': False}


# Global file manager instance
_file_manager = None

def get_file_manager() -> FileManager:
    """Get the global file manager instance."""
    global _file_manager
    if _file_manager is None:
        _file_manager = FileManager()
    return _file_manager 