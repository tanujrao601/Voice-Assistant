# Tanu

Your personal voice-activated assistant "Tanu" for Windows with multiple skills including app launching, web search, YouTube playback, and WhatsApp messaging.

## Features

### 1. **Open Applications**
Control your computer with voice commands to launch applications:
- Notepad
- Calculator
- Paint
- Web browsers (Chrome, Edge, Firefox)
- Office apps (Word, Excel, PowerPoint)
- WhatsApp
- Spotify

**Example commands:**
- "Open Notepad"
- "Launch Chrome"
- "Open Calculator"

### 2. **Web Search**
Search the web using Google or browse Wikipedia:
- **Example commands:**
  - "Search Python tutorial"
  - "Google voice assistants topic"
  - "Wikipedia artificial intelligence"

### 3. **YouTube Playback** 🎵
Play songs and videos on YouTube **automatically** by voice command:
- **Example commands:**
  - "Play Song Shape of You"
  - "Play Movie Avengers"
  - "Play Music Ed Sheeran"
  - "Play Video Python Programming Tutorial"
  - "Youtube Python Tutorial"
  - "Play Audio Today"
- Tanu will **automatically play** the first matching video on YouTube!

### 4. **WhatsApp Messaging** 💬
Send WhatsApp messages **automatically** via voice command (fully voice-controlled):
- **Example commands:**
  - "Whatsapp send to +1234567890 hello how are you"
  - "Whatsapp +1234567890 I am coming"
  - "Send whatsapp message to +1234567890 hey how are you"
  - "Message +1234567890 happy birthday"
- **Note:** Requires WhatsApp Web to be logged in. Messages are sent automatically after 2 minutes.
- Include country code with phone number (e.g., +1 for US, +91 for India)

### 5. **Email Sending** 📧
Send emails **automatically** via voice command (fully voice-controlled):
- **Example commands:**
  - "Send email to user@example.com subject meeting message let's meet tomorrow"
  - "Email to friend@email.com about project status the project is complete"
  - "Send mail to john@test.com urgent reminder check your inbox"
- **Setup required:** Set environment variables for your email credentials:
  ```bash
  set SENDER_EMAIL=your_email@gmail.com
  set SENDER_PASSWORD=your_app_password
  ```
- **Note:** For Gmail, use App Password (not regular password). Enable 2-factor authentication and generate App Password from Google Account settings.

## Installation

1. Install Python 3.x on your system
2. Install required dependencies:
```bash
pip install -r requirements.txt
```
Or manually:
```bash
pip install SpeechRecognition pywhatkit pyaudio
```

### Email Setup (Optional)
To enable email functionality, set environment variables:
- **Windows PowerShell:**
  ```powershell
  $env:SENDER_EMAIL="your_email@gmail.com"
  $env:SENDER_PASSWORD="your_app_password"
  ```
- **Windows Command Prompt:**
  ```cmd
  set SENDER_EMAIL=your_email@gmail.com
  set SENDER_PASSWORD=your_app_password
  ```
- **For Gmail users:** Create an App Password:
  1. Enable 2-Step Verification
  2. Go to Google Account → Security → App passwords
  3. Generate an app password for "Mail"
  4. Use this app password (not your regular password)

## Usage

Run Tanu:
```bash
python main.py
```

### Voice Commands
Once Tanu is running, you can:
1. **Speak** your command when it's listening
2. **Type** your command if speech recognition is not available or not installed

### Exit
Say or type "exit", "quit", or "stop" to stop Tanu.

## How It Works

Tanu uses a modular skill-based architecture. Each skill is in the `skills/` folder and can be easily extended:

- `open_app.py` - Application launcher
- `web_search.py` - Web search functionality
- `youtube_player.py` - YouTube playback
- `whatsapp_message.py` - WhatsApp messaging (automatic sending)
- `email_sender.py` - Email sending (automatic sending)

## Adding New Skills

To add a new skill:
1. Create a new Python file in the `skills/` folder
2. Define a class with:
   - `intent_phrases`: List of trigger phrases
   - `handle_intent(text)`: Method to process the command
3. Add a `register_skill()` function that returns your skill class

Example:
```python
class MySkill:
    intent_phrases = ['my trigger phrase']
    
    def handle_intent(self, text):
        # Process the command
        return True

def register_skill():
    return MySkill()
```

## Notes

- **YouTube**: Automatically plays the video directly on YouTube (no need to click!)
- **WhatsApp**: Automatically sends messages via WhatsApp Web (ensure WhatsApp Web is logged in). Messages are scheduled to send after 2 minutes.
- **Email**: Automatically sends emails via SMTP. Requires email credentials to be set as environment variables.
- **Microphone**: Tanu will calibrate for ambient noise on startup
- **Internet**: Required for YouTube playback, web search, WhatsApp messaging, and email sending
- **All features work entirely via voice commands** - no manual interaction needed!

## Troubleshooting

- If microphone doesn't work, Tanu falls back to text input
- Make sure your microphone is connected and enabled
- Check Windows microphone permissions
- Some commands may require internet connection (web search, YouTube, WhatsApp)

## License

Free to use and modify.

