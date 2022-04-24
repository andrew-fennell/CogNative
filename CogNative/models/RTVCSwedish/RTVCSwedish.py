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
from .utils.printing import colorize

from scipy.io import wavfile
import noisereduce as nr

import numpy as np
import librosa
import os

class RTVCSwedish:
    def __init__(self, src_lang):
        # SET UP PRETRAINED MODEL PATHS
        enc_weights = Path(f"CogNative/models/RTVC/saved_models/default/{src_lang}_encoder.pt")
        voc_weights = Path("CogNative/models/RTVC/saved_models/default/vocoder.pt")

        # LOAD PRETRAINED MODELS
        encoder.load_model(enc_weights)
        self.synthesizer = Synthesizer(Path("CogNative/models/RTVCSwedish/synthesizer/saved_models/swedish\\taco_pretrained"), low_mem=False, seed=1)
        vocoder.load_model(voc_weights)

        # Define variables
        self.file_path = None
        self.embed = None

    def encode_voice(self, file_path, save_embedding=False):
        """Creating embedding for voice using encoder."""
        if self.embed:
            pass

        # SET FILE PATH
        self.file_path = file_path
        in_wav = Path(self.file_path)
        assert os.path.exists(in_wav), "ERROR: File not found."

        print(colorize("Encoding voice...", 'success'))

        # SYNTHESIZE EXPECTED OUTPUT WAVEFORM
        enc_wav = audio.preprocess_wav(in_wav)
        og_wav, sampling_rate = librosa.load(in_wav)

        # Use Encoder to create embedding of input audio
        embed_wav = audio.preprocess_wav(og_wav, sampling_rate)
        self.embed = encoder.embed_utterance(embed_wav)
        if save_embedding:
            self.save_embedding()

    def set_file_path(self, file_path):
        # SET FILE PATH
        self.file_path = file_path
        in_wav = Path(self.file_path)
        assert os.path.exists(in_wav), "ERROR: File not found."

    def save_embedding(self):
        """Save current embedding to a checkpoint file."""
        np.savetxt(self.get_embedding_path(), self.embed)

    def load_embedding(self, embedding_path):
        """Load embedding from checkpoint file."""
        self.embed = np.loadtxt(embedding_path, dtype=float)

    def get_embedding_path(self):
        """Returns the embedding file location."""
        file_path_fmt = str(self.file_path).replace('\\', '/').split('/')[-1]
        embedding_path = f"CogNative/examples/saved_embeds/{file_path_fmt}.ckpt"
        return embedding_path

    def synthesize(self, text, out_path):
        """Synthesize output using synthesizer and vocoder."""
        with io.capture_output():
            specs = self.synthesizer.synthesize_spectrograms([text], [self.embed])

            # GENERATE UTTERANCE WITH VOCODER
            gen_wav = vocoder.infer_waveform(specs[0])
            gen_wav = np.pad(gen_wav, (0, self.synthesizer.sample_rate), mode="constant")

            # Output voice clone
            # Audio(out_wav, rate=synthesizer.sample_rate)
            print(colorize("\nExporting clone to", 'success'), colorize(f"/{out_path}", "path"))
            out_f = f"./{out_path}"
            aud.save_wav(gen_wav, out_f)

            rate, data = wavfile.read(out_path)
            reduced_noise = nr.reduce_noise(y=data, sr=rate, prop_decrease=0.7)
            wavfile.write(out_path, rate, reduced_noise)


if __name__ == "__main__":    
    # Initialize RTVC
    v = RTVCSwedish()
    v.encode_voice()
    
    # DEFINE OUTPUT TEXT FOR VOICE CLONE
    text = input("Enter text for voice clone:\n")

    while text != 'q':
        # DEFINE OUTPUT TEXT FOR VOICE CLONE
        text = input("Enter text for voice clone:\n")

        print(colorize('Synthesizing...', 'success'))
        v.synthesize(text, 'output')
