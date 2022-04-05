# Import libraries
from IPython.display import Audio
from IPython.utils import io

from .synthesizer.inference import Synthesizer
from .encoder import inference as encoder
from .encoder import audio as audio
from .vocoder import inference as vocoder
from .vocoder import audio as aud

from pathlib import Path
from pydub import AudioSegment
from colorama import Fore

from scipy.io import wavfile
import noisereduce as nr

import numpy as np
import librosa
import os

class RTVC:
    def __init__(self, path_to_models):
        # SET UP PRETRAINED MODEL PATHS
        enc_weights = Path(path_to_models + "/encoder.pt")
        voc_weights = Path(path_to_models + "/vocoder.pt")
        synth_dir = Path(path_to_models + "/synthesizer.pt")

        # LOAD PRETRAINED MODELS
        encoder.load_model(enc_weights)
        self.synthesizer = Synthesizer(synth_dir)
        vocoder.load_model(voc_weights)

        # Define variables
        self.file_path = None
        self.embed = None

    def encode_voice(self, file_path):
        # SET FILE PATH
        self.file_path = file_path
        in_wav = Path(self.file_path)
        assert os.path.exists(in_wav), f"{Fore.RED}ERROR: File not found."

        print(Fore.LIGHTGREEN_EX + "Loading requested file...")

        # SYNTHESIZE EXPECTED OUTPUT WAVEFORM
        enc_wav = audio.preprocess_wav(in_wav)
        og_wav, sampling_rate = librosa.load(in_wav)

        # Use Encoder to create embedding of input audio
        embed_wav = audio.preprocess_wav(og_wav, sampling_rate)
        self.embed = encoder.embed_utterance(embed_wav)
    
    def synthesize(self, text, out_path):
        with io.capture_output():
            specs = self.synthesizer.synthesize_spectrograms([text], [self.embed])

            # GENERATE UTTERANCE WITH VOCODER
            gen_wav = vocoder.infer_waveform(specs[0])
            gen_wav = np.pad(gen_wav, (0, self.synthesizer.sample_rate), mode="constant")

            # Output voice clone
            # Audio(out_wav, rate=synthesizer.sample_rate)
            print(Fore.LIGHTGREEN_EX + "\nExporting clone to", Fore.CYAN + f"/{out_path}")
            out_f = Path(f"./{out_path}")
            aud.save_wav(gen_wav, out_f)

            rate, data = wavfile.read(out_path)
            reduced_noise = nr.reduce_noise(y=data, sr=rate, prop_decrease=0.75)
            wavfile.write(out_path, rate, reduced_noise)


if __name__ == "__main__":    
    # Initialize RTVC
    v = RTVC()
    v.encode_voice()
    
    # DEFINE OUTPUT TEXT FOR VOICE CLONE
    text = input("Enter text for voice clone:\n")

    while text != 'q':
        # DEFINE OUTPUT TEXT FOR VOICE CLONE
        text = input("Enter text for voice clone:\n")

        print('Synthesizing...')
        v.synthesize(text, 'output')
