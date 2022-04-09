from pathlib import Path
from shutil import rmtree
import wave

from models.RTVC.RTVC import RTVC
from models.RTVC.utils.printing import colorize

# INITIALIZE RTVC
v = RTVC("models/RTVC/saved_models/default")

# SET INPUT AUDIO FILE PATH
file_path = Path(input("Enter input audio file path:\n"))
if not file_path.exists():
    print(colorize("ERROR: Path not found.", "error"))
    exit(1)
if not file_path.suffix == '.wav':
    print(colorize("ERROR: Enter an input .wav file", "error"))
    exit(1)

# ENTER TEXT
text = input("Enter text for voice clone:\n")
if not text[-1] == ".":
    print(colorize("ERROR: Punctuation missing.", "error"))
    exit(1)

# OUTPUT FILE PATH
output_path = Path(input("Enter output audio path:\n"))
if not output_path.parent.exists():
    print(colorize("ERROR: Directory not found.", "error"))
    exit(1)
if not output_path.suffix == '.wav':
    print(colorize("ERROR: Enter an output .wav file", "error"))
    exit(1)

v.set_file_path(file_path)

embedding_path = None
if Path(v.get_embedding_path()).exists():
    embedding = input("Use embedding? (y/n)\n")
    if embedding.lower() in ['y', 'yes']:
        embedding_path = v.get_embedding_path()
        if not Path(embedding_path).exists():
            print(colorize(f"ERROR: Embedding file ({embedding_path}) not found.", "error"))
            exit(1)
        if not Path(embedding_path).suffix == '.ckpt':
            print(colorize("ERROR: Enter a .ckpt embedding file", "error"))
            exit(1)

# ENCODE (sometimes this takes time, so it is after inputs)
if embedding_path:
    v.load_embedding(embedding_path)
else:
    v.encode_voice(file_path, save_embedding=True)

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
print(colorize('Synthesizing...', 'success'))
for i, text in enumerate(input_subs):
    out_path = f'{str(temp_output_path)}/output' + str(i) + '.wav'
    v.synthesize(text + '.', out_path)
    out_paths.append(str(out_path))

# JOIN ALL SUB-AUDIO FILES INTO ONE OUTPUT .wav
with wave.open(str(output_path), 'wb') as wav_out:
    for i, wav_path in enumerate(out_paths):
        with wave.open(wav_path, 'rb') as wav_in:
            if i == 0:
                wav_out.setparams(wav_in.getparams())
            wav_out.writeframes(wav_in.readframes(wav_in.getnframes()))

# REMOVE ALL TEMP FILES
rmtree(temp_output_path)

# PRINT SUCCESS
print(colorize(f"Clone output to {output_path}", "success"))
