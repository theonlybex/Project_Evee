# This is a script to track the conversation history between the user and the assistant

import json
import datetime
import pathlib

class conTracker:
    def __init__(self, email_address, message_id):
        self.email_address = email_address
        self.message_id = message_id
        self.conversation = None
        self._loaded = False
        self._ensure_loaded()

    def _ensure_loaded(self):
        """Load data only when needed"""
        if not self._loaded:
            try:
                logs_dir = pathlib.Path("gmail/logs")
                logs_dir.mkdir(parents=True, exist_ok=True)
                file_path = logs_dir / "requests.json"
                
                if file_path.exists() and file_path.stat().st_size > 0:
                    with open(file_path, "r") as f:
                        self.conversation = json.load(f)
                else:
                    self.conversation = {}
            except (FileNotFoundError, json.JSONDecodeError):
                self.conversation = {}
            
            self._loaded = True

    def save_conversation(self):
        """Save the conversation to the database"""
        try:
            with open(f"gmail/logs/requests.json", "w") as f:
                json.dump(self.conversation, f)
        except Exception as e:
            print(f"Error finding json file, creating new one: {e}")
            pathlib.Path("gmail/logs").mkdir(parents=True, exist_ok=True)
            with open(f"gmail/logs/requests.json", "w") as f:
                json.dump(self.conversation, f)

    def add_conversation(self, student_email, message_id, width, height, paper_type, price):
        """Add a new message to the conversation"""
        self.conversation[student_email] = {
            "student_email": student_email,
            "message_id": message_id,
            "status": "pending",
            "request_info": {
                "width": width,
                "height": height,
                "paper_type": paper_type,
                "request_price": price
            },
            "timestamp": datetime.datetime.now().isoformat()
        }
        self.save_conversation()

    def update_status(self, student_email, status):
        """Update the status of the conversation"""
        try:
            self.conversation[student_email]["status"] = status
        except KeyError:
            print(f"No conversation found for {student_email}")
            return False
        self.save_conversation()
        return True

    def get_conversation(self, student_email):
        """Get the conversation history"""
        try:
            return self.conversation[student_email]
        except KeyError:
            print(f"No conversation found for {student_email}")
            return None
    
