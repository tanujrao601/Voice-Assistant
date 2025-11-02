import subprocess

class OpenAppSkill:
    intent_phrases = [
        'open notepad', 'open calculator', 'launch paint', 'open chrome', 'open edge', 'open firefox', 'open whatsapp', 'launch spotify', 'open word', 'open excel', 'open powerpoint'
    ]
    app_map = {
        'notepad': 'notepad.exe',
        'calculator': 'calc.exe',
        'paint': 'mspaint.exe',
        'chrome': 'chrome.exe',
        'edge': 'msedge.exe',
        'firefox': 'firefox.exe',
        'whatsapp': r'C:\\Users\\%USERNAME%\\AppData\\Local\\WhatsApp\\WhatsApp.exe',
        'spotify': r'C:\\Users\\%USERNAME%\\AppData\\Roaming\\Spotify\\Spotify.exe',
        'word': r'C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE',
        'excel': r'C:\\Program Files\\Microsoft Office\\root\\Office16\\EXCEL.EXE',
        'powerpoint': r'C:\\Program Files\\Microsoft Office\\root\\Office16\\POWERPNT.EXE',
    }
    def handle_intent(self, text):
        for name, exe in self.app_map.items():
            if name in text.lower():
                subprocess.Popen([exe])
                print(f"[Opened {name.title()}]")
                return True
        print("[App not found]")
        return False

def register_skill():
    return OpenAppSkill()
