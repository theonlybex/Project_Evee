# This is a script that will check for new emails in the inbox and send response to requests

import imaplib
import email
import time
import threading
from email.header import decode_header
from requestMain import requestsMain
from dotenv import load_dotenv
load_dotenv()
import os
import asyncio



class EmailMonitor:
    def __init__(self, email_address, app_password):
        self.email_address = email_address
        self.app_password = app_password
        self.imap_server = "imap.gmail.com"
        self.imap_port = 993
        self.mailbox = None
        self.lock = threading.Lock()
        self.running = False
        self.last_uid = None  # Track last email UID to only process new ones
        
    def connect(self):
        """Connect to the Gmail IMAP server"""
        try:
            #connect to Gmail IMAP server
            self.mail = imaplib.IMAP4_SSL('imap.gmail.com', 993)

            #login with app password
            self.mail.login(self.email_address, self.app_password)

            #Select inbox
            self.mail.select('inbox')

            print(f"Connected to {self.email_address}")
            
            # Get the highest UID to ignore existing emails
            try:
                status, data = self.mail.search(None, 'ALL')
                if status == 'OK' and data[0]:
                    all_ids = data[0].split()
                    if all_ids:
                        # Simply use the highest email ID as starting point
                        # Convert last email ID to int for comparison
                        self.last_uid = int(all_ids[-1])
                        print(f"📌 Starting from email ID {self.last_uid} - ignoring existing emails")
            except Exception as e:
                print(f"⚠️ Could not set starting point: {e}")
                
            return True
        except Exception as e:
            print(f"Error connecting to Gmail: {e}")
            return False
    
    

    def requestProcessing(self, sender, email_body):
        """Call requestMain when new email arrives"""
        try:
            # Create instance of your requestMain class
            processor = requestsMain()
            
            # Call your existing function
            result = processor.requestsProcessing(sender, email_body)
            
            print(f"✅ Request processed: {result['success']}")
            
        except Exception as e:
            print(f"❌ Error calling requestMain: {e}")


    async def start_monitoring(self):
        """Start monitoring for new emails"""
        self.running = True

        while self.running:
            try:
                # Check if connection is still alive
                if not self.mail:
                    print("🔄 No connection, attempting to connect...")
                    if not self.connect():
                        print("❌ Failed to connect, waiting 30 seconds...")
                        await asyncio.sleep(30)
                        continue

                # Send NOOP to test connection
                try:
                    self.mail.noop()
                except:
                    print("🔄 Connection lost, reconnecting...")
                    self.reconnect()
                    continue

                #Send IDLE command to Gmail
                tag = self.mail._new_tag()
                self.mail.send(f'{tag} IDLE\r\n'.encode())

                #Wait for server response
                response = self.mail.readline()

                if b'+ idling' in response.lower():
                    print("📡 Gmail IDLE activated. Waiting for new emails...")
                    
                    #Waiting for notifications
                    while self.running:
                        try:
                            line = self.mail.readline()
                            
                            if not line:  # Connection dropped
                                print("🔄 Connection dropped, reconnecting...")
                                break

                            # Check for new messages
                            if b'EXISTS' in line:
                                print("🚨 New email detected!")

                                #Exit IDLE mode
                                self.mail.send(b'DONE\r\n')
                                self.mail.readline() # Read idle termination response

                                await self.check_new_emails()

                                #restart IDLE mode
                                break

                            #reconnect IDLE mode after timeout (29 minutes)
                            elif b'BYE' in line:
                                print("⏰ Gmail server timeout. Reconnecting...")
                                break
                        except Exception as inner_e:
                            print(f"⚠️ Error reading IDLE response: {inner_e}")
                            break
                        
            except Exception as e:
                print(f"❌ IDLE command error: {e}")
                print("🔄 Reconnecting in 10 seconds...")
                await asyncio.sleep(10)
                self.reconnect()
            
    async def check_new_emails(self):
        """Check for NEW emails only (after script started)"""
        try:
            # Search for all emails (we'll filter by UID)
            status, messages = self.mail.search(None, 'ALL')

            if status == 'OK' and messages[0]:
                email_ids = messages[0].split()

                # Process emails in reverse order (newest first)
                for email_id in reversed(email_ids):
                    current_id = int(email_id)
                    
                    # Only process if email ID is higher than our starting point
                    if self.last_uid is None or current_id > self.last_uid:
                        # Update last_uid to this email
                        self.last_uid = current_id
                        
                        # Fetch the full email
                        status, msg_data = self.mail.fetch(email_id, '(RFC822)')
                        
                        if status == 'OK':
                            # Parse the email
                            email_message = email.message_from_bytes(msg_data[0][1])

                            # Extract details
                            subject = self.decode_subject(email_message['Subject'])
                            sender = email_message['From']
                            email_body = self.extract_email_body(email_message)

                            print(f"📧 NEW email from: {sender}")
                            print(f"📝 Subject: {subject}")

                            # Check if the email is a request
                            if self.is_request(subject, sender):
                                print("🔍 This is a request. Processing...")
                                self.requestProcessing(sender, email_body)
                            else:
                                print("ℹ️ Not a request email - ignoring")
                    # else: email is older than our starting point, ignore it
                            
        except Exception as e:
            print(f"Error checking for new emails: {e}")

    def extract_email_body(self, email_message):
        """Safely extract email body from any email type"""
        try:
            if email_message.is_multipart():
                # Handle multipart emails (HTML + text)
                for part in email_message.walk():
                    if part.get_content_type() == "text/plain":
                        payload = part.get_payload(decode=True)
                        if payload:
                            return payload.decode('utf-8', errors='ignore')
                # If no text/plain part found, try any text part
                for part in email_message.walk():
                    if part.get_content_type().startswith("text/"):
                        payload = part.get_payload(decode=True)
                        if payload:
                            return payload.decode('utf-8', errors='ignore')
                return "[Multipart email - no readable content]"
            else:
                # Handle simple text emails
                payload = email_message.get_payload(decode=True)
                if payload:
                    return payload.decode('utf-8', errors='ignore')
                else:
                    return "[Empty email body]"
        except Exception as e:
            print(f"⚠️ Error extracting email body: {e}")
            return "[Could not extract email content]"

    def is_request(self, subject, sender):
        """Check if the email is a request"""
        required_keywords = ['request', 'order', 'printing', 'cube']
        subject_lower = subject.lower() if subject else ""
        return any(keyword in subject_lower for keyword in required_keywords)
    
    def decode_subject(self, subject):
        """Decode email subject"""
        if subject:
            decoded = decode_header(subject)[0]
            if decoded[1]:
                return decoded[0].decode(decoded[1])
            return str(decoded[0])
        return ""
    
    def reconnect(self):
        """Reconnect to server"""
        try:
            if self.mail:
                try:
                    self.mail.close()
                    self.mail.logout()
                except:
                    pass
                self.mail = None
        except:
            pass
        
        print("⏳ Waiting 5 seconds before reconnecting...")
        time.sleep(5)
        
        for attempt in range(3):
            print(f"🔄 Reconnection attempt {attempt + 1}/3...")
            if self.connect():
                print("✅ Reconnected successfully!")
                return True
            else:
                print(f"❌ Attempt {attempt + 1} failed")
                if attempt < 2:
                    time.sleep(10)  # Wait longer between attempts
        
        print("💔 All reconnection attempts failed")
        return False
    
    def stop(self):
        """Stop monitoring"""
        self.running = False
        try:
            self.mail.send(b'DONE\r\n')  # Exit IDLE
            self.mail.close()
            self.mail.logout()
        except:
            pass

async def main():
    monitor = EmailMonitor(
        email_address = os.getenv("GMAIL_EMAIL"), 
        app_password = os.getenv("GMAIL_APP_PASSWORD")
        )
    if monitor.connect():
        try:
            await monitor.start_monitoring()
        except KeyboardInterrupt:
            print("Stopping monitoring...")
            monitor.stop()
            print("Monitoring stopped.")
            return
    else:
        print("Failed to connect to Gmail. Exiting...")

if __name__ == "__main__":
    asyncio.run(main())
    
    