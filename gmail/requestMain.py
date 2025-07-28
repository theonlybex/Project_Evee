# This script will be used to reply to student requests about CUBE operations.
import sys
import os
import asyncio
import csv
import json
from typing import List, Optional, Dict, Any
from pathlib import Path
from dataclasses import dataclass, asdict
from datetime import datetime

from PyPDF2 import PdfReader
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from pydantic import BaseModel
from browser_use import ActionResult, Agent, Controller, BrowserSession
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()

    
class requestsMain:
    def __init__(self):
        #initiating the LLM
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            api_key = os.getenv("OPENAI_API_KEY"),
            temperature=0.0
        )

        #Configure the browserSession
        self.browser_session = BrowserSession(
            headless=False,
            window_size={"width": 1920, "height": 1080},
            viewport_size={"width": 1920, "height": 1080}
        )
    def priceCalculator(self, width: int, height: int, paper_type: str):
        """Calculate the price of the request"""
        if paper_type == "glassy":
            return width * height * 0.01 * 1000 #1000 is the price per square meter
        else:
            return width * height * 0.005 * 1000 #1000 is the price per square meter
        
    # Register the function as a tool
    tools = [
        {
            "type": "function",
            "function": {
                "name": "priceCalculator",
                "description": "Calculate price based on width, height and material type",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "width": {"type": "number", "description": "Width in units"},
                        "height": {"type": "number", "description": "Height in units"},
                        "material": {"type": "string", "enum": ["standard", "premium", "luxury"]}
                    },
                    "required": ["width", "height"]
                }
            }
        }
    ]
        
    def requestsProcessing(self, sender, email_body):
        """Login to the email account"""

        #Define the task for the agent
        task = f"""
            You are a helpful assistant for processing CUBE printing requests.
            Do not put your analysis in the reply, just provide the reply.

            Here is the email content from a student request:
            ---
            FROM: {sender}
            CONTENT: {email_body}
            ---

            Analyze this email content and extract:
            - The width of the request (in cm)
            - The height of the request (in cm)
            - The paper type (glassy or standard)
            - Any attached files mentioned

            If any required information is missing, generate a reply asking for:
            - Missing width/height/paper type
            - Instructions on how to send a proper request

            If all information is present, generate a reply with:
            - Thank the student for the request from the CUBE team
            - Confirm the request is valid
            - Calculate price using: width × height × paper_type (glassy=0.01×1000, standard=0.005×1000)
            - Provide the total price in dollars
            - Respond in the same language as the original request
            """

        print("🚀 Processing email content...")
        print("📧 From:", sender)

        try:
            # Step 3: Process with LLM directly (no browser)
            reply_content = self.llm.predict(task)  # ✅ Direct text processing

            print("✅ Reply generated successfully!")

            #Send the reply
            self.send_reply_via_smtp(sender, "CUBE Request Response", reply_content)
            
            
            return {
                'success': True,
                'message': 'Email processed and reply sent',
                'reply_content': reply_content
            }
        except Exception as e:
            print(f"❌ Error: {e}")
            return {
                'success': False,
                'message': f'Login failed: {str(e)}',
                'history': None
            }
        
    def send_reply_via_smtp(self, recipient, subject, reply_content):
        """Send reply email via SMTP using app password"""
        try:
            # Email configuration
            sender_email = os.getenv("GMAIL_EMAIL")  # Your Gmail address
            app_password = os.getenv("GMAIL_APP_PASSWORD")  # Your app password
            
            # Create message
            message = MIMEMultipart()
            message["From"] = sender_email
            message["To"] = recipient
            message["Subject"] = f"Re: {subject}"
            
            # Add body
            message.attach(MIMEText(reply_content, "plain"))
            
            # Connect and send
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login(sender_email, app_password)
            server.send_message(message)
            server.quit()
            
            print(f"✅ Reply sent to {recipient}")
            return True
            
        except Exception as e:
            print(f"❌ Error sending email: {e}")
            return False



