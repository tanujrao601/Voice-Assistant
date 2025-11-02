import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

class EmailSenderSkill:
    intent_phrases = [
        'send email', 'email', 'send mail', 'mail', 'email to', 'send email to'
    ]
    
    def __init__(self):
        # You can set these via environment variables or configuration
        # For Gmail, you'll need an App Password (not regular password)
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.sender_email = os.getenv('SENDER_EMAIL', '')
        self.sender_password = os.getenv('SENDER_PASSWORD', '')
    
    def extract_email_details(self, text):
        """Extract recipient, subject, and body from voice command."""
        text_l = text.lower().strip()
        
        # Pattern 1: "send email to [email] subject [subject] message [body]"
        pattern1 = r'send\s+email\s+to\s+([^\s@]+@[^\s@]+\.\w+)\s+subject\s+(.+?)\s+message\s+(.+)$'
        match1 = re.search(pattern1, text_l)
        if match1:
            recipient = match1.group(1).strip()
            subject = match1.group(2).strip()
            body = match1.group(3).strip()
            return recipient, subject, body
        
        # Pattern 2: "email to [email] subject [subject] [body]"
        pattern2 = r'email\s+to\s+([^\s@]+@[^\s@]+\.\w+)\s+subject\s+(.+?)\s+(.+)$'
        match2 = re.search(pattern2, text_l)
        if match2:
            recipient = match2.group(1).strip()
            subject = match2.group(2).strip()
            body = match2.group(3).strip()
            return recipient, subject, body
        
        # Pattern 3: "send mail to [email] [subject] [body]" - simpler format
        pattern3 = r'send\s+mail\s+to\s+([^\s@]+@[^\s@]+\.\w+)\s+(.+?)\s+(.+)$'
        match3 = re.search(pattern3, text_l)
        if match3:
            recipient = match3.group(1).strip()
            # Try to split subject and body (subject is usually shorter)
            remaining = match3.group(2).strip()
            # Assume first few words are subject, rest is body
            parts = remaining.split(' ', 1)
            if len(parts) == 2:
                subject = parts[0]
                body = parts[1] + ' ' + match3.group(3).strip()
            else:
                subject = remaining
                body = match3.group(3).strip()
            return recipient, subject, body
        
        # Pattern 4: "send email to [email] about [subject] [body]"
        pattern4 = r'send\s+email\s+to\s+([^\s@]+@[^\s@]+\.\w+)\s+about\s+(.+?)\s+(.+)$'
        match4 = re.search(pattern4, text_l)
        if match4:
            recipient = match4.group(1).strip()
            subject = match4.group(2).strip()
            body = match4.group(3).strip()
            return recipient, subject, body
        
        # Pattern 5: More flexible - "email [email] [subject] [body]"
        pattern5 = r'email\s+([^\s@]+@[^\s@]+\.\w+)\s+(.+)$'
        match5 = re.search(pattern5, text_l)
        if match5:
            recipient = match5.group(1).strip()
            remaining = match5.group(2).strip()
            # Try to extract subject (first few words) and body
            words = remaining.split()
            if len(words) > 1:
                # First 3-5 words as subject, rest as body
                subject_words = min(5, len(words) // 2)
                subject = ' '.join(words[:subject_words])
                body = ' '.join(words[subject_words:])
            else:
                subject = remaining
                body = "No message body provided"
            return recipient, subject, body
        
        return None, None, None
    
    def send_email(self, recipient, subject, body):
        """Send email using SMTP."""
        if not self.sender_email or not self.sender_password:
            return False, "Email credentials not configured. Please set SENDER_EMAIL and SENDER_PASSWORD environment variables."
        
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = recipient
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))
            
            # Connect to SMTP server and send
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()  # Enable encryption
            server.login(self.sender_email, self.sender_password)
            text = msg.as_string()
            server.sendmail(self.sender_email, recipient, text)
            server.quit()
            
            return True, f"Email sent successfully to {recipient}"
        except smtplib.SMTPAuthenticationError:
            return False, "Authentication failed. Check your email and password (use App Password for Gmail)."
        except Exception as e:
            return False, f"Error sending email: {str(e)}"
    
    def handle_intent(self, text):
        text_l = text.lower()
        
        # Check if command contains email-related keywords
        if 'email' not in text_l and 'mail' not in text_l:
            return False
        
        # Extract recipient, subject, and body
        recipient, subject, body = self.extract_email_details(text)
        
        if recipient and subject and body:
            success, result_msg = self.send_email(recipient, subject, body)
            
            if success:
                print(f"[Email] {result_msg}")
                print(f"[To]: {recipient}")
                print(f"[Subject]: {subject}")
                print(f"[Body]: {body}")
            else:
                print(f"[Email Error] {result_msg}")
                print("[Note: For Gmail, use App Password, not regular password]")
                print("[Set environment variables: SENDER_EMAIL and SENDER_PASSWORD]")
            return success
        
        # If we couldn't parse, provide helpful message
        print("[Email] Could not parse recipient, subject, and message body.")
        print("[Usage examples:]")
        print("  - 'send email to user@example.com subject meeting message let's meet tomorrow'")
        print("  - 'email to friend@email.com about project status the project is complete'")
        print("  - 'send mail to john@test.com urgent reminder check your inbox'")
        return False

def register_skill():
    return EmailSenderSkill()

