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

from scipy.io import wavfile
import noisereduce as nr

print(os.getcwd())

# SET UP PRETRAINED MODEL PATHS
enc_weights = Path("Real-Time-Voice-Cloning/saved_models/default/encoder.pt")
voc_weights = Path("Real-Time-Voice-Cloning/saved_models/default/vocoder.pt")
synth_dir = Path("Real-Time-Voice-Cloning/saved_models/default/synthesizer.pt")

# LOAD PRETRAINED MODELS
encoder.load_model(enc_weights)
synthesizer = Synthesizer(synth_dir)
vocoder.load_model(voc_weights)

# DEFINE OUTPUT TEXT FOR VOICE CLONE
filename_txt = input(Fore.LIGHTGREEN_EX + "Enter name of input text file:\n")
in_txt = Path(f"Clone_Tests/{filename_txt}.txt")
assert os.path.exists(in_txt), f"{Fore.RED}ERROR: File not found."
text_file = open(f"Clone_Tests/{filename_txt}.txt", "r")
text_data = text_file.read()
text_file.close()
print(text_data)

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
    specs = synthesizer.synthesize_spectrograms([text_data], [embed])

# GENERATE UTTERANCE WITH VOCODER
gen_wav = vocoder.infer_waveform(specs[0])
gen_wav = np.pad(gen_wav, (0, synthesizer.sample_rate), mode="constant")

# Output voice clone
# Audio(out_wav, rate=synthesizer.sample_rate)
print(Fore.LIGHTGREEN_EX + "\nExporting clone to", Fore.CYAN + "Clone_Tests")
out_f = Path(f"Clone_Tests/{filename}_Clone.wav")
aud.save_wav(gen_wav, out_f)

rate, data = wavfile.read(f"Clone_Tests/{filename}_Clone.wav")
reduced_noise = nr.reduce_noise(y=data, sr=rate, prop_decrease=0.75)
wavfile.write(f"Clone_Tests/{filename}_Clone_Post.wav", rate, reduced_noise)
