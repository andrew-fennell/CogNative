from pathlib import Path
from shutil import rmtree
import wave
import re
from pydub import AudioSegment

from .models.RTVC.RTVC import RTVC
from .models.RTVC.utils.printing import colorize

from .backend.backend import speech_transcription
from .backend.modules.translation import translation
from .backend.modules.STT import STT


# GET ARGS
# make args list containing only actual arguments
import sys
args = sys.argv[1:]

# SET INPUT AUDIO FILE PATH
if '-sampleAudio' in args and args.index('-sampleAudio') < len(args):
    file_path = Path(args[args.index('-sampleAudio')+1])
else:
    file_path = Path(input("Enter input audio file path:\n"))

# DETECT LANGUAGE OF INPUT AUDIO
st_detect = STT()
src_lang = st_detect.detect_language(file_path)

# INITIALIZE RTVC
print("================================================")
v = RTVC("CogNative/models/RTVC/saved_models/default", src_lang)
print("================================================")
    
if not file_path.exists():
    print(colorize("ERROR: Path not found.", "error"))
    exit(1)
if not file_path.suffix == '.wav':
    print(colorize("ERROR: Enter an input .wav file", "error"))
    exit(1)

# CHOOSE TEXT OR AUDIO INPUT
if '-synType' in args and args.index('-synType') < len(args):
    synthesis_type = args[args.index('-synType')+1].lower()
else:
    synthesis_type = input("Synthesize from text or audio? (text/audio)\n").lower()

if synthesis_type == "audio":
    # INITIALIZE SPEECH_TRANSCRIPTION
    st = speech_transcription(google_creds='../credentials.json')

    # CHOOSE AUDIO FOR STT
    if '-dialogueAudio' in args and args.index('-dialogueAudio') < len(args):
        audio_path = Path(args[args.index('-dialogueAudio')+1])
    else:
        audio_path = Path(input("Enter the audio file path:\n"))
    
    if not audio_path.exists():
        print(colorize("ERROR: Path not found.", "error"))
        exit(1)
    if not audio_path.suffix == '.wav':
        print(colorize("ERROR: Enter an input .wav file", "error"))
        exit(1)
    
    text = st.transcribe_audio(str(audio_path), dest_lang='english')

else:
    # CHOOSE TEXT
    if '-dialogueText' in args and args.index('-dialogueText') < len(args):
        text = args[args.index('-dialogueText')+1]
    else:
        text = input("Enter text for voice clone:\n")
    
    tr = translation()
    text = tr.translate_to(text, 'english')

# OUTPUT FILE PATH
if '-out' in args and args.index('-out') < len(args):
    output_path = Path(args[args.index('-out')+1])
else:
    output_path = Path(input("Enter output audio path:\n"))
    
if not output_path.parent.exists():
    print(colorize("ERROR: Directory not found.", "error"))
    exit(1)
if not output_path.suffix == '.wav':
    print(colorize("ERROR: Enter an output .wav file", "error"))
    exit(1)

v.set_file_path(file_path)

# EMBEDDING PATH
embedding_path = None
if Path(v.get_embedding_path()).exists():
    if '-useExistingEmbed' in args and args.index('-useExistingEmbed') < len(args):
        embedding = args[args.index('-useExistingEmbed')+1]
    else:
        embedding = input("Use embedding? (y/n)\n")
        
    if embedding.lower() in ['y', 'yes']:
        embedding_path = v.get_embedding_path()
        if not Path(embedding_path).exists():
            print(colorize(f"ERROR: Embedding file ({embedding_path}) not found.", "error"))
            exit(1)
        if not Path(embedding_path).suffix == '.ckpt':
            print(colorize("ERROR: Enter a .ckpt embedding file", "error"))
            exit(1)

# SEPARATE TEXT BY PUNCTUATION
punctuation_regex = '\. |\? |\! |\; |\: | \— |\—|\.\.\. |\.|\?|\!|\;|\:|\.\.\.'
punctuation = re.findall(punctuation_regex, text)
input_subs_split = re.split(punctuation_regex, text)
input_subs_split.pop()

# JOIN SENTENCES TO BE SYNTHESIZED TOGETHER
input_subs = []
for i in range(0, len(input_subs_split)):
    input_subs.append(input_subs_split[i] + punctuation[i])

# ENCODE (sometimes this takes time, so it is after inputs)
if embedding_path:
    v.load_embedding(embedding_path)
else:
    v.encode_voice(file_path, save_embedding=True)

# OUTPUT AUDIO FILE PATHS
temp_output_path = Path('temp')
if not temp_output_path.exists():
    temp_output_path.mkdir()
out_paths = []

# SYNTHESIZE OUTPUT AUDIO
print(colorize('Synthesizing...', 'success'))
silence_to_cut = 600 #measured in ms
for i, text in enumerate(input_subs):
    out_path = f'{str(temp_output_path)}/output' + str(i) + '.wav'
    v.synthesize(text, out_path)
    audio_segment = AudioSegment.from_wav(out_path)
    audio_segment_duration = audio_segment.duration_seconds
    audio_segment_reduced = audio_segment[:(audio_segment_duration - silence_to_cut)]
    audio_segment_reduced.export(out_path, format="wav")
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
