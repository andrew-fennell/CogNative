import os
import wave

from models.RTVC.RTVC import RTVC

# INITIALIZE RTVC
v = RTVC("models/RTVC/saved_models/default")

# SET INPUT AUDIO FILE PATH
file_path = input("Enter input audio file path:\n")
assert os.path.exists(file_path), "ERROR: Path not found."

# ENTER TEXT
text = input("Enter text for voice clone:\n")
assert text[-1] == ".", "ERROR: Punctuation missing."

# OUTPUT FILE PATH
output_path = input("Enter output audio path:\n")
if "/" in output_path:
    output_temp = output_path.split("/")
    output_temp.pop(-1)
    output_temp = "/".join(output_temp)
    assert os.path.exists(output_temp), "ERROR: Path not found."

# ENCODE (sometimes this takes time, so it is after inputs)
v.encode_voice(file_path)

# SEPARATE TEXT BY PERIOD
input_subs = text.split('. ')

# JOIN <span> SENTENCES TO BE SYNTHESIZED TOGETHER
span = 3
input_subs = [". ".join(input_subs[i:i+span]) for i in range(0, len(input_subs), span)]

# OUTPUT AUDIO FILE PATHS
temp_output_path = 'temp'
if not os.path.exists(temp_output_path):
    os.mkdir(temp_output_path)
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
for f in os.listdir(temp_output_path):
    os.remove(os.path.join(temp_output_path, f))
os.rmdir(temp_output_path)