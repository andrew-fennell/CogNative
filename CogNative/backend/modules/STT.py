import io
import os

import wave
from google.cloud import speech
from pathlib import Path
from shutil import rmtree
from pydub import AudioSegment

from ...models.RTVC.utils.printing import colorize
from .languages import available_languages

# Set GOOGLE_APPLICATION_CREDENTIALS if
# it is not already set in the current environment
if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credentials.json"

class STT:
    def __init__(self, google_creds='credentials.json'):
        """Speech-to-Text module that converts audio input to text output.

        Arguments:
        google_creds -- .json file with Google Cloud Speech credentials

        Note: Language of previously transcribed audio can be found under
                    the variable "STT.source_language".
        """

        # Set GOOGLE_APPLICATION_CREDENTIALS if
        # it is not already set in the current environment
        if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = google_creds

        # Variable initialization
        self.source_language = 'english'

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

        primary_lang = available_languages[self.source_language]["stt"]

        config = speech.RecognitionConfig(language_code=primary_lang,
                      alternative_language_codes=['en-US', 'es-MX', 'fr-FR', 'de-DE', 'sv-SE'],
                      enable_automatic_punctuation=True,
                      audio_channel_count=num_chans,
                      encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16)
        
        response = client.recognize(request={"config": config, "audio": audio})

        text = response.results[0].alternatives[0].transcript
        lang = response.results[0].language_code

        lang_keys = list(available_languages.keys())
        lang_codes = [available_languages[x]["stt"] for x in lang_keys]
        for i in range(len(lang_codes)):
            # Update self.source_language with the language
            # used to transcribe the given audio
            if lang_codes[i].split('-')[0] == lang.split('-')[0]:
                self.source_language = lang_keys[i]

        # Saves text data associated with audio file path within the object
        self.stt_data[file_path] = text

        return text
    
    def detect_language(self, audio_path):
        """Auto-detect language in a given audio file."""

        if not Path(audio_path).suffix == '.wav':
            print(colorize("ERROR: Enter an input .wav file", "error"))
            exit(1)

        temp_dir = Path('temp_detect')
        if not temp_dir.exists():
            temp_dir.mkdir()

        audio = AudioSegment.from_wav(audio_path)
        audio_duration = audio.duration_seconds*1000
        duration = 25000 if audio_duration > 25000 else audio_duration
        audio_reduced = audio[:duration]
        audio_reduced.export(f"{str(temp_dir)}/detect.wav", format="wav")

        self.speech_to_text(f"{str(temp_dir)}/detect.wav")

        # REMOVE ALL TEMP FILES
        rmtree(temp_dir)

        return self.source_language

    def get_transcriptions(self):
        """Returns all transcriptions performed by this object.

        Output:
        dict[file_path]: transcription of file_path
        """
        return self.stt_data

if __name__ == "__main__":

    # Enter an audio file
    audio_file = input("Input a audio file path: ")

    # Instantiate STT() object
    s = STT()

    text = s.speech_to_text(audio_file)
    print(f"{audio_file}: {text}")
