from stt import STT
from translation import translation

class speech_translation:

    def __init__(self):
        # Instantiate variables
        self.data = {}

    def translate_audio(self, audio_file_path, src_lang, dest_lang):
        """Convert audio in source language to text in destination language."""
        
        # Instantiate STT and Translation objects
        stt = STT.STT(source_language=src_lang)
        tr = translation.translation()

        # Convert audio file to text (in the same language)
        src_text = stt.speech_to_text(audio_file_path)

        # Translated text from source language to destination language
        dest_text = tr.translate(src_text, src_lang, dest_lang)

        return dest_text

if __name__ == "__main__":
    translator = speech_translation()

    file_path = input("Enter your audio file path: ")
    src_lang = input("Source language: ")
    dest_lang = input("Destination language: ")

    translated_text = translator.translate_audio(file_path, src_lang, dest_lang)
    
    print(translated_text)
