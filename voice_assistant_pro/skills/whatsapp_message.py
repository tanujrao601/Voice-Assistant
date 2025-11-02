import re
import pywhatkit as pwt
from datetime import datetime

class WhatsAppMessageSkill:
    intent_phrases = [
        'whatsapp', 'send message', 'message', 'whatsapp message', 'send whatsapp',
        'send whatsapp message', 'whatsapp send'
    ]
    
    def extract_contact_and_message(self, text):
        """Extract contact name/phone number and message from various command formats."""
        text_l = text.lower().strip()
        
        # Pattern 1: "whatsapp send to [name/phone] [message]" or "send whatsapp to [name/phone] [message]"
        pattern1 = r'(?:whatsapp\s+send|send\s+whatsapp)\s+to\s+(.+?)\s+(.+)$'
        match1 = re.search(pattern1, text_l)
        if match1:
            contact = match1.group(1).strip()
            message = match1.group(2).strip()
            return contact, message
        
        # Pattern 2: "whatsapp [name/phone] [message]" - simpler format
        pattern2 = r'whatsapp\s+(.+?)\s+(.+)$'
        match2 = re.search(pattern2, text_l)
        if match2:
            contact = match2.group(1).strip()
            message = match2.group(2).strip()
            return contact, message
        
        # Pattern 3: "send message to [name/phone] [message]" or "message to [name/phone] [message]"
        pattern3 = r'(?:send\s+)?message\s+to\s+(.+?)\s+(.+)$'
        match3 = re.search(pattern3, text_l)
        if match3:
            contact = match3.group(1).strip()
            message = match3.group(2).strip()
            return contact, message
        
        # Pattern 4: "message [name/phone] [message]" - even simpler
        pattern4 = r'^message\s+(.+?)\s+(.+)$'
        match4 = re.search(pattern4, text_l)
        if match4:
            contact = match4.group(1).strip()
            message = match4.group(2).strip()
            return contact, message
        
        # Pattern 5: "send to [name/phone] [message]"
        pattern5 = r'^send\s+to\s+(.+?)\s+(.+)$'
        match5 = re.search(pattern5, text_l)
        if match5:
            contact = match5.group(1).strip()
            message = match5.group(2).strip()
            return contact, message
        
        return None, None
    
    def get_phone_number(self, contact):
        """Convert contact name or phone string to phone number format."""
        # Remove all non-digit characters except +
        phone = re.sub(r'[^\d+]', '', contact)
        
        # If it's already a phone number (has digits)
        if phone and phone.replace('+', '').isdigit():
            return phone
        
        # If it's a name, try to extract phone number from it
        # For now, assume the user provides phone number with country code
        # You can extend this to use a contacts database
        return contact
    
    def send_whatsapp_message(self, phone, message):
        """Send WhatsApp message using pywhatkit."""
        try:
            # Get current time and add 2 minutes delay (pywhatkit requirement)
            now = datetime.now()
            hour = now.hour
            minute = now.minute + 2  # Send after 2 minutes
            
            # Handle minute overflow
            if minute >= 60:
                minute -= 60
                hour = (hour + 1) % 24
            
            # Clean phone number
            phone_clean = re.sub(r'[^\d+]', '', phone)
            if not phone_clean:
                return False, "Invalid phone number format"
            
            # Ensure phone has country code (add + if not present and assume it's a local number)
            if not phone_clean.startswith('+'):
                # You might want to add default country code here
                # For now, require user to say country code
                phone_clean = '+' + phone_clean if phone_clean[0] != '0' else phone_clean
            
            # Send message using pywhatkit
            # Note: pywhatkit requires WhatsApp Web to be logged in and browser to be open
            print(f"[Preparing to send WhatsApp message to {phone_clean} at {hour:02d}:{minute:02d}]")
            pwt.sendwhatmsg(phone_clean, message, hour, minute)
            
            return True, f"Message will be sent to {phone_clean} at {hour:02d}:{minute:02d}"
        except Exception as e:
            return False, f"Error sending WhatsApp message: {str(e)}"
    
    def handle_intent(self, text):
        text_l = text.lower()
        
        # Check if command contains WhatsApp-related keywords
        if 'whatsapp' not in text_l and 'message' not in text_l and 'send' not in text_l:
            return False
        
        # Extract contact name/phone and message
        contact, message = self.extract_contact_and_message(text)
        
        if contact and message:
            phone = self.get_phone_number(contact)
            success, result_msg = self.send_whatsapp_message(phone, message)
            
            if success:
                print(f"[WhatsApp] {result_msg}")
                print(f"[Message]: {message}")
                print("[Note: Make sure WhatsApp Web is open and logged in]")
            else:
                print(f"[WhatsApp Error] {result_msg}")
            return success
        
        # If we couldn't parse, provide helpful message
        print("[WhatsApp] Could not parse contact and message.")
        print("[Usage examples:]")
        print("  - 'whatsapp send to +1234567890 hello there'")
        print("  - 'send whatsapp message to John hello'")
        print("  - 'whatsapp +1234567890 this is a test message'")
        return False

def register_skill():
    return WhatsAppMessageSkill()
