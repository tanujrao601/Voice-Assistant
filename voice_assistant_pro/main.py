import os
import sys
import importlib
import importlib.util
import threading

# Add speech recognition import (optional)
try:
    import speech_recognition as sr
except Exception:
    sr = None

class VoiceAgent:
    def __init__(self):
        self.skills = {}
        self.load_skills()

    def load_skills(self):
        """Dynamically load all skill modules from the skills/ folder."""
        skill_dir = os.path.join(os.path.dirname(__file__), 'skills')
        if not os.path.isdir(skill_dir):
            print(f"[Warning] skills directory not found: {skill_dir}")
            return

        for fname in os.listdir(skill_dir):
            if fname.endswith('.py') and not fname.startswith('_'):
                name = fname[:-3]
                path = os.path.join(skill_dir, fname)
                try:
                    spec = importlib.util.spec_from_file_location(f"skills.{name}", path)
                    if spec and spec.loader:
                        mod = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(mod)
                    else:
                        print(f"[Warning] could not load spec for {fname}")
                        continue
                except Exception as e:
                    print(f"[Error] failed to import {fname}: {e}")
                    continue

                if hasattr(mod, 'register_skill'):
                    try:
                        handle = mod.register_skill()
                    except Exception as e:
                        print(f"[Error] register_skill() failed in {fname}: {e}")
                        continue
                    if hasattr(handle, 'intent_phrases') and hasattr(handle, 'handle_intent'):
                        for phrase in handle.intent_phrases:
                            if isinstance(phrase, str):
                                # normalize stored phrases to lowercase for matching
                                self.skills[phrase.lower()] = handle
                    else:
                        print(f"[Warning] skill {fname} missing intent_phrases or handle_intent")

    def handle_voice_command(self, text):
        """Try all skill handlers; fallback to typing or failure."""
        if not text:
            return None
        text_l = text.lower()
        for phrase, skill in self.skills.items():
            if phrase in text_l:
                try:
                    result = skill.handle_intent(text)
                    if result is not None:
                        print(result)
                    return result
                except Exception as e:
                    print(f"[Error] skill handler raised: {e}")
                    return None
        print(f"[No skill handler found for]: {text}")
        return None

def listen_loop(agent):
    if sr is None:
        print("[Notice] speech_recognition not installed. Install with: pip install SpeechRecognition")
        print("[Fallback] Use text input (type 'exit', 'quit', or 'stop' to quit).")
        try:
            while True:
                cmd = input("You (type): ")
                if not cmd:
                    continue
                if cmd.strip().lower() in ('exit', 'quit', 'stop'):
                    print("Goodbye.")
                    break
                agent.handle_voice_command(cmd)
        except KeyboardInterrupt:
            print("\nExiting.")
        return

    recognizer = sr.Recognizer()
    # adjust for ambient noise once
    try:
        with sr.Microphone() as source:
            print("Calibrating microphone for ambient noise... (stay quiet)")
            recognizer.adjust_for_ambient_noise(source, duration=1.5)
    except Exception as e:
        print(f"[Error] Cannot access microphone: {e}")
        print("[Fallback] Use text input (type 'exit', 'quit', or 'stop' to quit).")
        # fallback to typed input
        try:
            while True:
                cmd = input("You (type): ")
                if not cmd:
                    continue
                if cmd.strip().lower() in ('exit', 'quit', 'stop'):
                    print("Goodbye.")
                    break
                agent.handle_voice_command(cmd)
        except KeyboardInterrupt:
            print("\nExiting.")
        return

    print("=" * 60)
    print("[Tanu - Ready to listen!]")
    print("Say 'exit', 'quit', or 'stop' to stop Tanu")
    print("Press Ctrl+C to force exit")
    print("=" * 60)
    print()
    try:
        while True:
            try:
                with sr.Microphone() as source:
                    print("Listening...")
                    audio = recognizer.listen(source, timeout=6, phrase_time_limit=8)
                try:
                    text = recognizer.recognize_google(audio)
                    print(f"You (heard): {text}")
                    if text.strip().lower() in ('exit', 'quit', 'stop'):
                        print("Goodbye.")
                        break
                    agent.handle_voice_command(text)
                except sr.UnknownValueError:
                    # couldn't understand audio
                    print("[Could not understand audio]")
                except sr.RequestError as e:
                    print(f"[Speech API error]: {e}")
                    # optionally fallback to keyboard input
            except sr.WaitTimeoutError:
                # no speech detected within timeout
                # continue listening loop
                continue
    except KeyboardInterrupt:
        print("\nExiting.")

if __name__ == "__main__":
    agent = VoiceAgent()
    listen_loop(agent)