import speech_recognition as sr

class STT:
    def __init__(self, source_language="english", engine="google"):
        """Speech-to-Text module that converts audio input to text output.

        Arguments:
        source_language -- The language of the audio (currently only 'english')
        engine -- Engine used to perform speech recognition (currently only 'google')
        """

        # Variable initialization
        self.source_language = source_language
        self.engine = engine

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

            # Choose which engine to use to perform STT
            # Generate text from audio
            if self.engine == "google":
                text = self.r.recognize_google(data)
            
            # If an engine that is not supported was entered
            else:
                raise(Exception('Please select a supported speech recognition engine.'))
            
        # Saves text data associated with audio file path within the object
        self.stt_data[file_path] = text

        return text


if __name__ == "__main__":
    s = STT()
    audio_file = input("Input a audio file path: ")

    text = s.speech_to_text(audio_file)
    print(f"{audio_file}: {text}")
