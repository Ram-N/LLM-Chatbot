import speech_recognition as sr
from deep_translator import GoogleTranslator
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import io
import time
import platform
import langdetect
from langdetect import detect, LangDetectException


# Import appropriate sound module based on OS
if platform.system() == 'Windows':
    import winsound
    def make_beep():
        frequency = 1000  # Frequency in Hz
        duration = 500   # Duration in milliseconds
        winsound.Beep(frequency, duration)
else:
    import os
    def make_beep():
        os.system('play -nq -t alsa synth 0.5 sine 1000') if platform.system() == 'Linux' else \
            os.system('afplay /System/Library/Sounds/Ping.aiff') if platform.system() == 'Darwin' else None

offer_to_help = {'en': "How can I help you?",
    'hi': "मैं आपकी कैसे मदद कर सकता हूँ?",
    'ta': "நான் எப்படி உங்களுக்கு உதவ முடியும்?",
    'te': "నేను మీకు ఎలా సహాయం చేయగలను?",
    'bn': "আমি কিভাবে সাহায্য করতে পারি?",
    'ml': "എനിക്ക് എങ്ങനെ നിങ్ങളെ സഹായിക്കാനാകും?"}



class LanguageAssistant:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.translator = GoogleTranslator(source='auto', target='en')

    def translate_text(self, text, source_lang='en', target_lang='hi'):
        """
        Translate text between any two languages
        """
        try:
            # Create translator for this specific translation
            translator = GoogleTranslator(source=source_lang, target=target_lang)
            translated_text = translator.translate(text)
            print(f"\nOriginal ({source_lang}): {text}")
            print(f"Translated ({target_lang}): {translated_text}")
            return translated_text
        except Exception as e:
            print(f"Translation error: {str(e)}")
            return text  # Return original text if translation fails
    
    def speak(self, text, source_lang='en', target_lang='hi'):
        """
        Convert text to speech with translation support
        """
        try:
            # Translate if source and target languages are different
            if source_lang != target_lang:
                text = self.translate_text(text, source_lang, target_lang)
            
            # Create an in-memory bytes buffer
            mp3_fp = io.BytesIO()
            
            # Generate speech
            print(f"\nGenerating speech in {target_lang}")
            tts = gTTS(text=text, lang=target_lang, slow=False)
            tts.write_to_fp(mp3_fp)
            mp3_fp.seek(0)
            
            # Convert to AudioSegment and play
            print("Speaking...")
            audio = AudioSegment.from_mp3(mp3_fp)
            play(audio)
            
        except Exception as e:
            print(f"Speech generation error: {str(e)}")
        finally:
            mp3_fp.close()


    def listen_translate_and_speak(self, user_lang='hi'):
        """
        Listen to speech, translate, and speak responses
        """
        try:
            with sr.Microphone() as source:
                print("\nAdjusting for ambient noise... Please wait...")
                self.recognizer.adjust_for_ambient_noise(source, duration=2)
                
                self.speak(offer_to_help[user_lang], user_lang, user_lang)
                # Initial prompt in multiple languages
                if user_lang=='ta':
                    self.speak("பீப்புக்குப் பிறகு பேசவும்", 'ta', 'ta')
                else:
                    self.speak("बीप के बाद बोलें", 'hi', 'hi')
    
                
                print("\n🎤 Listening...")
                print("\n🔊 BEEP! Please speak in...")
                make_beep()
                time.sleep(0.5)  # Small pause after beep

                audio = self.recognizer.listen(source, timeout=10, phrase_time_limit=10)
                print("Processing...", user_lang)
                
                # Try both Hindi and Tamil recognition
                results = {}
                
                # Try Hindi
                if user_lang=='hi':
                    try:
                        hindi_text = self.recognizer.recognize_google(audio, language="hi-IN")
                        results['hi'] = {
                            'text': hindi_text,
                            'translation': self.translator.translate(hindi_text)
                        }
                    except (sr.UnknownValueError, sr.RequestError):
                        results['hi'] = None

                # Try Tamil
                if user_lang=='ta':
                    try:
                        tamil_text = self.recognizer.recognize_google(audio, language="ta-IN")
                        results['ta'] = {
                            'text': tamil_text,
                            'translation': self.translator.translate(tamil_text)
                        }
                    except (sr.UnknownValueError, sr.RequestError):
                        results['ta'] = None

                # Process and speak results
                if any(results.get(lang) for lang in ['hi', 'ta']):
                    print("\n=== Results ===")
                    print(results)
                    
                    if 'hi' in results:
                        print("\n📌 Hindi Recognition:")
                        print(f"Text: {results['hi']['text']}")
                        print(f"Translation: {results['hi']['translation']}")
                        
                        self.speak("I heard this in Hindi:", 'en')
                        self.speak(results['hi']['text'], 'hi')
                        time.sleep(0.5)
                        self.speak(results['hi']['translation'], 'en')
                    
                    if 'ta' in results:
                        print("\n📌 Tamil Recognition:")
                        print(f"Text: {results['ta']['text']}")
                        print(f"Translation: {results['ta']['translation']}")
                        
                        self.speak("I heard this in Tamil:", 'en')
                        self.speak(results['ta']['text'], 'ta')
                        time.sleep(0.5)
                        self.speak(results['ta']['translation'], 'en')
                
                else:
                    msg = "Sorry, I couldn't recognize the speech in either Hindi or Tamil"
                    print(msg)
                    self.speak(msg, 'en')
                    
        except sr.WaitTimeoutError:
            msg = "No speech detected within timeout period"
            print(msg)
            self.speak(msg, 'en')
        except Exception as e:
            print(f"Error: {e}")

    def demo_speech(self):
        """
        Demonstrate text-to-speech capabilities in different languages
        """
        print("\n=== Choices with Our App ===")
        
        # Hindi demo
        hindi_text = """
        1. आप इस ऐप का उपयोग करके अपना बैलेंस जान सकते हैं।
        2. किसी मित्र या परिवार को पैसे भेज सकते हैं।
        3.अपने पिछले 2 लेन-देन देख सकते हैं।
        4. अपने पैसों की सामान्य जानकारी प्राप्त कर सकते हैं।

        """
        print(f"\nHindi: {hindi_text}")
        self.speak(hindi_text, 'hi', 'hi')
        
        # Tamil demo
        tamil_text = """
        1.     இந்த ஆப்ஸைப் பயன்படுத்தி உங்கள் பணம் இருப்பை அறியலாம்.
        2. நண்பர் அல்லது குடும்பத்தினருக்கு பணம் அனுப்பலாம்.
        3. கடைசி 2 பண பரிவர்த்தனைகளைப் பார்க்கலாம்.
        4. உங்கள் பணத்தின் பொதுவான தகவலை அறியலாம்.

        """
        print(f"\nTamil: {tamil_text}")
        self.speak(tamil_text, 'ta', target_lang='ta')


    def detect_native_language(self):
        """
        Detect the user's native language by iterating through a list of options and listening for their response.
        """

        choices = [
            ('en', "Continue in English?"),
            ('hi', "Continue in Hindi?"),
            ('ta', "Continue in Tamil"), 
            ("te", "Continue in Telugu?"),
            ('bn', 'Bengali?'),
            ('ml', 'Malayalam')
            ]


        for lang, prompt in choices:
            try:
                with sr.Microphone() as source:
                    self.recognizer.adjust_for_ambient_noise(source, duration=2)
                    self.speak(prompt, 'en', target_lang=lang)
                    print(f"\n🎤 Listening for response in {lang}...")
                    audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
                    print("Processing...")
                    user_text = self.recognizer.recognize_google(audio, language=lang)
                    user_language = detect(user_text)
                    print(f"\nDetected user's native language: {user_language}")
                    if user_language == lang:
                        self.speak(f"Okay, let's {prompt}.", 'en', user_language)
                        return user_language

            except (sr.UnknownValueError, sr.RequestError, LangDetectException):
                continue

        # If no language could be detected, default to English
        return 'en'


def main():
    print("Multilingual Speech Assistant")
    print("----------------------------")
    
    # Installation check
    try:
        import gtts
        import pydub
        from deep_translator import GoogleTranslator
        import langdetect
    except ImportError:
        print("\nPlease install required packages:")
        print("pip install gTTS pydub deep-translator langdetect")
        return

    assistant = LanguageAssistant()
    user_language='hi'

    user_language = assistant.detect_native_language()

    while True:
        print("\nOptions:")
        print("1. Change native language")
        print("2. Start conversation (speech recognition and translation)")
        print("3. List App Options Hindi, Tamil")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ")
        
        if choice == '1':
            user_language = assistant.detect_native_language()
            if user_language != 'en':
                assistant.speak(f"Okay, let's continue in {user_language}.", 'en', user_language)
        elif choice == '2':
            assistant.listen_translate_and_speak(user_language)
        elif choice == '3':
            assistant.demo_speech()
        elif choice == '4':
            assistant.speak("हमारे साथ बैंकिंग करने के लिए धन्यवाद", "hi", target_lang=user_language)
            # assistant.speak("எங்களுடன் வங்கிச் சேவையை பயன்படுத்தியதற்கு நன்றி", "ta")
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    print("Before running this script, install required packages:")
    print("pip install SpeechRecognition deep-translator gtts pydub langdetect")
    print("\nNote: For Windows users with pyaudio installation issues:")
    print("pip install pipwin")
    print("pipwin install pyaudio")
    main()