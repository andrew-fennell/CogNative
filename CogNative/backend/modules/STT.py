import io
import os

import wave
from google.cloud import speech
from pathlib import Path
from shutil import rmtree
from pydub import AudioSegment
from datetime import datetime, timedelta

from ...models.RTVC.utils.printing import colorize
from .languages import available_languages
from .audio_split import split_audio

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

    def speech_to_text(self, file_path, output_path=None):
        """Converts audio data to text.

        Keyword arguments:
        file_path -- audio file path (.wav, .flac, .aiff)
        """

        # Check if output_path is possible (before time
        # is spent with the following transcription)
        if output_path:
            if not Path(output_path).parent.exists():
                print(colorize(f"The directory {Path(output_path).parent} does not exist."))
                exit(1)

        audio_paths = split_audio(file_path)

        self.stt_data[file_path] = []
        start_time = datetime.now()
        for complete, audio_path in enumerate(audio_paths):
            # Speech Recognition initializations
            client = speech.SpeechClient()

            with io.open(audio_path, "rb") as audio_file:
                content = audio_file.read()
                audio = speech.RecognitionAudio(content=content)

            with wave.open(audio_path) as audio_file:
                num_chans = audio_file.getnchannels()

            primary_lang = available_languages[self.source_language]["stt"]

            config = speech.RecognitionConfig(language_code=primary_lang,
                        alternative_language_codes=['en-US', 'es-MX', 'fr-FR', 'de-DE', 'sv-SE'],
                        enable_automatic_punctuation=True,
                        audio_channel_count=num_chans,
                        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16)
            
            response = client.recognize(request={"config": config, "audio": audio})

            try:
                text = response.results[0].alternatives[0].transcript
                lang = response.results[0].language_code

                lang_keys = list(available_languages.keys())
                lang_codes = [available_languages[x]["stt"] for x in lang_keys]
                for i in range(len(lang_codes)):
                    # Update self.source_language with the language
                    # used to transcribe the given audio
                    if lang_codes[i].split('-')[0] == lang.split('-')[0]:
                        self.source_language = lang_keys[i]
            except Exception:
                if len(audio_paths) > 1:
                    print("An exception has occurred. STT will continue with next section.")
                    continue
                else:
                    raise Exception

            # Saves text data associated with audio file path within the object
            self.stt_data[file_path].append(text)

            # Print which (i) audio path is being transcribed
            percent_complete = round(100 * (complete+1) / len(audio_paths), 2)
            time_since_start = datetime.now() - start_time
            time_remaining = (1 / (percent_complete / 100)) * time_since_start - time_since_start
            time_remaining = str(time_remaining).split('.')[0]
            print(f"Transcribing: [{percent_complete}%] (est. {time_remaining} remaining)")
        
        self.stt_data[file_path] = ' '.join(self.stt_data[file_path])

        if output_path:
            with open(output_path, 'w') as f:
                f.write(self.stt_data[file_path])

        return self.stt_data[file_path]
    
    def detect_language(self, audio_path):
        """Auto-detect language in a given audio file."""

        if not Path(audio_path).suffix == '.wav':
            print(colorize("ERROR: Enter an input .wav file", "error"))
            exit(1)

        temp_dir = Path(f"temp_detect_{Path(audio_path).with_suffix('').name}")
        if not temp_dir.exists():
            temp_dir.mkdir()

        audio = AudioSegment.from_wav(audio_path)
        audio_duration = audio.duration_seconds*1000
        duration = 10000 if audio_duration > 10000 else audio_duration
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
    audio_file = input("Input a audio file path (.wav): ")

    # Enter output file path for text
    output_path = input("Input output file audio path (.txt): ")

    # Instantiate STT() object
    s = STT()

    start_time = datetime.now()

    text = s.speech_to_text(audio_file, output_path=output_path)
    print(f"{audio_file}: {text}")

    end_time = datetime.now()

    print('Duration: {}'.format(end_time - start_time))
