import webbrowser
import re

class WebSearchSkill:
    intent_phrases = [
        'search', 'google', 'wikipedia', 'weather', 'directions'
    ]
    def handle_intent(self, text):
        text = text.lower()
        if text.startswith('search') or text.startswith('google'):
            m = re.search(r'search(?: for)? (.+)', text)
            if m:
                q = m.group(1)
                url = f'https://www.google.com/search?q={q.replace(' ', '+')}'
                webbrowser.open(url)
                print(f'[Google search for: {q}]')
                return True
        if 'wikipedia' in text:
            m = re.search(r'wikipedia(?: for| about)? (.+)', text)
            if m:
                topic = m.group(1)
                url = f'https://en.wikipedia.org/wiki/{topic.replace(' ', '_')}'
                webbrowser.open(url)
                print(f'[Wikipedia for: {topic}]')
                return True
        print('[WebSearchSkill: No match]')
        return False

def register_skill():
    return WebSearchSkill()
