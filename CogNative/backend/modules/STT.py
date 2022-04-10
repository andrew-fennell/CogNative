import speech_recognition as sr

from .languages import available_languages



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

        # Speech Recognition initializations
        self.r = sr.Recognizer()

        # Data variables
        self.stt_data = {}

    def speech_to_text(self, file_path):
        """Converts audio data to text.

        Keyword arguments:
        file_path -- audio file path (.wav, .flac, .aiff)
        """

        with sr.AudioFile(file_path) as source:
            # Extract data from audio file
            data = self.r.record(source)
            # Generate text from audio
            text = self.r.recognize_google(data, language=self.source_language)

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
