import re

class YouTubePlayerSkill:
    intent_phrases = [
        'play song', 'play music', 'play video', 'play on youtube', 'youtube play',
        'open youtube', 'youtube song', 'play audio', 'youtube', 'play movie'
    ]
    
    def extract_query(self, text):
        """Extract the song/movie name from various command formats."""
        original_text = text.lower()
        
        # Patterns ordered by specificity (most specific first)
        # We match against original text to preserve structure
        patterns = [
            (r'youtube\s+(.+)', True),  # "youtube songname"
            (r'play\s+(?:song|music|video|audio|movie)\s+(.+)', True),  # "play song name"
            (r'play\s+on\s+youtube\s+(.+)', True),  # "play on youtube name"
            (r'play\s+(.+)\s+youtube', True),  # "play name youtube"
            (r'play\s+(.+)', False),  # Less specific, needs validation
        ]
        
        for pattern, always_valid in patterns:
            match = re.search(pattern, original_text)
            if match:
                query = match.group(1).strip()
                # Clean up the query
                query = re.sub(r'\s+', ' ', query)  # Normalize whitespace
                
                # Remove filler words
                fillers = ['the', 'a', 'an', 'on', 'please', 'now']
                words = query.split()
                query = ' '.join([w for w in words if w not in fillers])
                
                # Remove trailing common words
                query = re.sub(r'\s+(song|music|video|audio|movie|on|youtube)$', '', query)
                
                # Validate query
                if query and len(query.split()) > 0:
                    # If it's a less specific pattern, make sure it's reasonable
                    if not always_valid:
                        # If query seems too short or is likely a false match, skip
                        if len(query) < 3:
                            continue
                    return query
        
        return None
    
    def handle_intent(self, text):
        try:
            import pywhatkit as pwt
        except ImportError:
            print('[Error] pywhatkit not installed. Install with: pip install pywhatkit')
            print('[Falling back to basic YouTube search]')
            import webbrowser
            query = self.extract_query(text)
            if query:
                url = f'https://www.youtube.com/results?search_query={query.replace(" ", "+")}'
                webbrowser.open(url)
                print(f'[Searching YouTube: {query}]')
                return True
            return False
        
        # Extract the query using the improved method
        query = self.extract_query(text)
        
        if query:
            try:
                # Use pywhatkit to play the video directly on YouTube
                pwt.playonyt(query)
                print(f'[Playing on YouTube: {query}]')
                return True
            except Exception as e:
                print(f'[Error playing video: {e}]')
                # Fallback to search
                import webbrowser
                url = f'https://www.youtube.com/results?search_query={query.replace(" ", "+")}'
                webbrowser.open(url)
                print(f'[Searching YouTube: {query}]')
                return True
        
        print('[YouTubePlayerSkill: Could not extract song/video name]')
        return False

def register_skill():
    return YouTubePlayerSkill()
