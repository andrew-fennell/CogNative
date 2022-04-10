import io
import os

import wave
from google.cloud import speech


from .languages import available_languages

# Set GOOGLE_APPLICATION_CREDENTIALS if
# it is not already set in the current environment
if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credentials.json"

class STT:
    def __init__(self, source_language="english"):
        """Speech-to-Text module that converts audio input to text output.

        Arguments:
        source_language -- The language of the audio
        engine -- Engine used to perform speech recognition
        """

        if source_language not in available_languages.keys():
            raise (Exception("Please select a supported language."))

        # Variable initialization
        self.source_language = available_languages[source_language]["stt"]

        # Data variables
        self.stt_data = {}

    def speech_to_text(self, file_path):
        """Converts audio data to text.

        Keyword arguments:
        file_path -- audio file path (.wav, .flac, .aiff)
        """

        # Speech Recognition initializations
        client = speech.SpeechClient()

        with io.open(file_path, "rb") as audio_file:
            content = audio_file.read()
            audio = speech.RecognitionAudio(content=content)
        
        with wave.open(file_path) as audio_file:
            num_chans = audio_file.getnchannels()
        
        config = speech.RecognitionConfig(language_code=self.source_language,
                      enable_automatic_punctuation=True,
                      audio_channel_count=num_chans,
                      encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16)
        
        response = client.recognize(request={"config": config, "audio": audio})

        text = response.results[0].alternatives[0].transcript

        # Saves text data associated with audio file path within the object
        self.stt_data[file_path] = text

        return text

    def get_transcriptions(self):
        """Returns all transcriptions performed by this object.

        Output:
        dict[file_path]: transcription of file_path
        """
        return self.stt_data


if __name__ == "__main__":

    # Language that will be in the audio file
    language = input("Enter your language (see backend/speech-to-text/README.md): ")

    # Enter an audio file
    audio_file = input("Input a audio file path: ")

    # Instantiate STT() object
    s = STT(source_language=language)

    text = s.speech_to_text(audio_file)
    print(f"{audio_file}: {text}")
