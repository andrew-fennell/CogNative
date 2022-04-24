from pathlib import Path
from pydub import AudioSegment
import re

from ...models.RTVC.utils.printing import colorize


def mp3_to_wav(audio_path):
    """Converts an .mp3 file into a .wav file."""
    file_check = Path(audio_path).exists()
    assert file_check, print(
        colorize(f"Audio file does not exist. ({audio_path})", "error")
    )

    # input audio file
    print(
        colorize(
            f"Audio file found ({audio_path}).",
            "success",
        )
    )
    clip = AudioSegment.from_file(audio_path, format="mp3")
    new_audio_path = Path(audio_path).with_suffix(".wav")
    clip.export(new_audio_path, format="wav")

    return str(new_audio_path)

def split_text(text):
    punctuation_regex = '\. |\? |\! |\; |\: | \— |\—|\.\.\. |\.|\?|\!|\;|\:|\.\.\.'

    # CHECKS INPUT VALIDITY
    if len(text) == 0:
        print(colorize("Please enter text into the split_text function.", "error"))
        exit(1)
    
    # ADD PUNCTUATION TO END OF TEXT, IF NEEDED
    if text[-1] not in punctuation_regex:
        text += '.'

    # SEPARATE TEXT BY PUNCTUATION
    punctuation = re.findall(punctuation_regex, text)
    input_subs_split = re.split(punctuation_regex, text)
    input_subs_split.pop()

    # JOIN SENTENCES TO BE TOGETHER
    input_subs = []
    for i in range(0, len(input_subs_split)):
        input_subs.append(input_subs_split[i] + punctuation[i])
    return input_subs

def punctuation_spacer(text):
    punctuation_list = ['...', '.', '?', '!', ';', '—']
    for x in punctuation_list:
        text = text.replace(x, x + " ")
    return text

if __name__ == "__main__":
    audio_path = input("Name of mp3 audio file:\n")
    assert Path(audio_path).exists, print(
        colorize(f"File does not exist. ({audio_path})", "error")
    )
    print(colorize(f"Exported to: {mp3_to_wav(audio_path)}", "success"))
