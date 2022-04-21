from .modules import STT, translation


class speech_transcription:
    def __init__(self, google_creds='credentials.json'):
        # Instantiate variables
        self.data = {}
        self.google_creds = google_creds

    def transcribe_audio(self, audio_file_path, dest_lang):
        """Convert audio in source language to text in destination language."""

        # Instantiate STT and Translation objects
        stt = STT.STT(google_creds=self.google_creds)
        tr = translation.translation()

        # Convert audio file to text (in the same language)
        src_text = stt.speech_to_text(audio_file_path)

        return src_text


if __name__ == "__main__":
    translator = speech_transcription()

    file_path = input("Enter your audio file path: ")
    dest_lang = input("Destination language: ")

    translated_text = translator.transcribe_audio(file_path, dest_lang)

    print(translated_text)
