# Import libraries
from IPython.display import Audio
from IPython.utils import io

from synthesizer.inference import Synthesizer
from encoder import inference as encoder
from encoder import audio as audio
from vocoder import inference as vocoder
from vocoder import audio as aud

from pathlib import Path
from pydub import AudioSegment
from colorama import Fore

import numpy as np
import librosa
import os

print(os.getcwd())

# SET UP PRETRAINED MODEL PATHS
enc_weights = Path("encoder.pt")
voc_weights = Path("vocoder.pt")
synth_dir = Path("synthesizer.pt")

# LOAD PRETRAINED MODELS
encoder.load_model(enc_weights)
synthesizer = Synthesizer(synth_dir)
vocoder.load_model(voc_weights)

# DEFINE OUTPUT TEXT FOR VOICE CLONE
text = input("Enter text for voice clone:\n")
assert text[-1] == ".", f"{Fore.RED}ERROR: Punctuation missing."

# ENCODE INPUT WAVEFORM
filename = input(Fore.LIGHTGREEN_EX + "Enter name of input audio file:\n")
in_wav = Path(f"Clone_Tests/{filename}.wav")
assert os.path.exists(in_wav), f"{Fore.RED}ERROR: File not found."

print(Fore.LIGHTGREEN_EX + "Loading requested file...")

# SYNTHESIZE EXPECTED OUTPUT WAVEFORM
enc_wav = audio.preprocess_wav(in_wav)
og_wav, sampling_rate = librosa.load(in_wav)

# Use Encoder to create embedding of input audio
embed_wav = audio.preprocess_wav(og_wav, sampling_rate)
embed = encoder.embed_utterance(embed_wav)

with io.capture_output() as captured:
    specs = synthesizer.synthesize_spectrograms([text], [embed])

# GENERATE UTTERANCE WITH VOCODER
gen_wav = vocoder.infer_waveform(specs[0])
gen_wav = np.pad(gen_wav, (0, synthesizer.sample_rate), mode="constant")

# Output voice clone
# Audio(out_wav, rate=synthesizer.sample_rate)
print(Fore.LIGHTGREEN_EX + "\nExporting clone to", Fore.CYAN + "Clone_Tests")
out_f = Path(f"Clone_Tests/{filename}_Clone.wav")
aud.save_wav(gen_wav, out_f)
