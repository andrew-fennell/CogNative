from pathlib import Path
from shutil import rmtree
import wave

from models.RTVC.RTVC import RTVC

# INITIALIZE RTVC
#v = RTVC("models/RTVC/saved_models/default")

# SET INPUT AUDIO FILE PATH
file_path = Path(input("Enter input audio file path:\n"))
assert file_path.exists(), "ERROR: Path not found."
assert file_path.suffix == '.wav', "ERROR: Enter an input .wav file"

# ENTER TEXT
text = input("Enter text for voice clone:\n")
assert text[-1] == ".", "ERROR: Punctuation missing."

# OUTPUT FILE PATH
output_path = Path(input("Enter output audio path:\n"))
assert output_path.parent.exists(), "ERROR: Directory not found."
assert output_path.suffix == '.wav', "ERROR: Enter an output .wav file"

# ENCODE (sometimes this takes time, so it is after inputs)
v.encode_voice(file_path)

# SEPARATE TEXT BY PERIOD
input_subs = text.split('. ')

# JOIN <span> SENTENCES TO BE SYNTHESIZED TOGETHER
span = 2
input_subs = [". ".join(input_subs[i:i+span]) for i in range(0, len(input_subs), span)]

# OUTPUT AUDIO FILE PATHS
temp_output_path = Path('temp')
if not temp_output_path.exists():
    temp_output_path.mkdir()
out_paths = []

# SYNTHESIZE OUTPUT AUDIO
print('Synthesizing...')
for i, text in enumerate(input_subs):
    out_path = f'{temp_output_path}/output' + str(i) + '.wav'
    v.synthesize(text + '.', out_path)
    out_paths.append(out_path)

# JOIN ALL SUB-AUDIO FILES INTO ONE OUTPUT .wav
with wave.open(output_path, 'wb') as wav_out:
    for i, wav_path in enumerate(out_paths):
        with wave.open(wav_path, 'rb') as wav_in:
            if i == 0:
                wav_out.setparams(wav_in.getparams())
            wav_out.writeframes(wav_in.readframes(wav_in.getnframes()))

# REMOVE ALL TEMP FILES
rmtree(temp_output_path)