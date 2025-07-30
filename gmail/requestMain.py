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
from conTracker import conTracker

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
        if paper_type == "glossy":
            return width * height * (3/12)
        else:
            return width * height * (2/12)
        
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

    def followUp(self, sender, email_body, existing_conv, current_message_id=None, cc=None):
        """Handles followup messages"""
        print(f"Processing follow-up from {sender}")
        
        # Make tracker instance
        tracker = conTracker(sender, "")

        # Use the current message ID (student's "yes" reply) for proper threading
        # This ensures our confirmation appears as a reply to their "yes" email
        reply_to_message_id = current_message_id or ''
        
        # Check if they agree to the price
        email_body = email_body.lower()
        positive_keywords = ["yes", "agree", "accept", "confirm", "ok", "sure", "i agree", "i accept", "i confirm", "i ok", "i sure"]
        negative_keywords = ["no", "disagree", "reject", "cancel", "deny", "i don't agree", "i don't accept", "i don't confirm", "i don't ok", "i don't sure"]
        
        #Check if they agree to the price
        if any(keyword in email_body for keyword in positive_keywords):
            print("🔍 Student agreed to the price")

            #Change the status to confirmed
            tracker.update_status(sender, "confirmed")

            # Send threaded confirmation email (reply to original quote)
            confirmation_message = f"""Thank you for confirming your order!

                Your CUBE printing request has been confirmed and will be processed shortly.

                Order Details:
                - Dimensions: {existing_conv['request_info']['width']} x {existing_conv['request_info']['height']}
                - Paper Type: {existing_conv['request_info']['paper_type']}
                - Price: ${existing_conv['request_info']['request_price']}

                We'll notify you when your print is ready for pickup.

                Best regards,
                CUBE Team"""

            self.send_reply_via_smtp(sender, "CUBE Request Confirmed", confirmation_message, reply_to_message_id, cc or "")


        elif any(keyword in email_body for keyword in negative_keywords):
            print("🔍 Student disagreed to the price")
            # They declined
            print("❌ Student declined the order")
            tracker.update_status(sender, "declined")
            
            # Send threaded decline acknowledgment
            decline_message = """We understand you've decided not to proceed with this printing request.

                            If you change your mind or have any questions, please don't hesitate to contact us.

                            Thank you for considering CUBE for your printing needs.

                            Best regards,
                            CUBE Team"""
            
            self.send_reply_via_smtp(sender, "CUBE Request Declined", decline_message, reply_to_message_id, cc or "")
            
        else:
            print("🔍 Student did not respond to the price")
            # Follow up is unclear
            print("❌ Follow up is unclear")
            tracker.update_status(sender, "pending")
            
            # Send threaded clarification request
            clarification_message = f"""We received your response but weren't sure if you'd like to proceed with your printing request.

                Order Details:
                - Dimensions: {existing_conv['request_info']['width']} x {existing_conv['request_info']['height']}
                - Paper Type: {existing_conv['request_info']['paper_type']}
                - Price: ${existing_conv['request_info']['request_price']}

                Please reply with:
                - "Yes" to confirm your order
                - "No" to decline

                Best regards,
                CUBE Team"""
            
            self.send_reply_via_smtp(sender, "CUBE Request - Please Clarify", clarification_message, reply_to_message_id, cc or "")
            
            
        
    def requestsProcessing(self, sender, email_body, message_id, cc):
        """Reply to requests"""

        # Create tracker instance
        tracker = conTracker(sender, message_id)

        # Check if we've talked to a student before 
        existing_conv = tracker.get_conversation(sender)

        #Check if the conversation is already in the database
        if existing_conv is not None:
            print("🔍 Conversation already in the database")
            print(f"Status: {tracker.get_conversation(sender)['status']}")

            #Check if we are waiting for the student response
            if tracker.get_conversation(sender)['status'] == "pending":
                print("🔍 This is a follow up request!")
                #Send the follow-up
                return self.followUp(sender, email_body, existing_conv)
            else:
                # Could be a new request from the same Student
                print("Previous conversation was completed")

        # At this point it is a new request
        print(f"New Request from {sender}")



        #Define the task for the agent
        task = f"""
            You are a helpful assistant for processing CUBE printing requests.
            Do not put your analysis in the reply, just provide the reply.

            Here is the email content from a student request:
            ---
            FROM: {sender}
            CONTENT: {email_body}
            ---

            Analyze this email content and extract the following information:
            {{
                "extracted_data": {{
                    "width": <number or null>,
                    "height": <number or null>, 
                    "paper_type": "<glossy/standard or null>",
                    "price": <calculated price or null>,
                    "all_info_present": <true/false>
                }},
                "reply_message": "<your email reply text here>"
            }}

            If any required information is missing, generate a reply asking for:
            - Missing width/height/paper type
            - Instructions on how to send a proper request

            If all information is present, generate a reply with:
            - Thank the student for the request from the CUBE team
            - Confirm the request is valid
            - Calculate price using: width * height * (3/12) for glossy and width * height * (2/12) for standard
            - Provide the total price in dollars
            - Respond in the same language as the original request
            - Ask user to respond with "yes" or "no" to the price
            """

        print("🚀 Processing email content...")
        print("📧 From:", sender)

        try:
            # Step 3: Process with LLM directly (no browser)
            reply_content = self.llm.predict(task)  # ✅ Direct text processing

            print("✅ Reply generated successfully!")

            #Extract the data from the reply
            extracted_data = json.loads(reply_content)
            width = extracted_data["extracted_data"]["width"]
            height = extracted_data["extracted_data"]["height"]
            paper_type = extracted_data["extracted_data"]["paper_type"]
            price = extracted_data["extracted_data"]["price"]

            #Check if the data is valid
            if width is None or height is None or paper_type is None or price is None:
                print("❌ Invalid data, sending reply to ask for missing information")
                # Still send the reply asking for more info
                reply_message = extracted_data["reply_message"] 
                self.send_reply_via_smtp(sender, "CUBE Request Response", reply_message, message_id, cc)
                return {
                    'success': False,
                    'message': 'Invalid data, sent reply asking for missing information'
                }


            #Send the reply
            reply_message = extracted_data["reply_message"]
            self.send_reply_via_smtp(sender, "CUBE Request Response", reply_message, message_id, cc)

            #Save the conversation
            tracker.add_conversation(sender, message_id, width, height, paper_type, price)
            
            #Update the conversation history
            tracker.update_status(sender, "pending")
            
            
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
        
    def send_reply_via_smtp(self, recipient, subject, reply_content, message_id, cc):
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
            
            if message_id:
                message["In-Reply-To"] = message_id
                message["References"] = message_id

            if cc:
                cc_list = [email.strip() for email in cc.split(',')]
                sender_email = os.getenv("GMAIL_EMAIL")
                cc_list = [email for email in cc_list if email != sender_email]
                if cc_list:
                    message["Cc"] = ", ".join(cc_list)
            
            
            
            # Add body
            message.attach(MIMEText(reply_content, "plain"))
            
            #Create list of all recipients
            all_recipients = [recipient]
            if cc:
                cc_list = [email.strip() for email in cc.split(',')]
                sender_email = os.getenv("GMAIL_EMAIL")
                cc_list = [email for email in cc_list if email != sender_email]
                all_recipients.extend(cc_list)


            # Connect and send
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login(sender_email, app_password)
            server.send_message(message)
            server.quit()
            
            print(f"✅ Reply sent to {all_recipients}")
            return True
            
        except Exception as e:
            print(f"❌ Error sending email: {e}")
            return False



