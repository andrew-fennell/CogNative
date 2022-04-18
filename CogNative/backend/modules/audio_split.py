from pydub import AudioSegment
from pydub.silence import split_on_silence
from colorama import Fore
import os

# user input for audio file + file existence check
aud_file = input("Enter name of audio file: ")
file_check = os.path.exists(f"Clone_Tests/Raw/{aud_file}.mp3")
assert file_check, print(f"{Fore.YELLOW}Please move audio file to 'Clone_Tests/Raw/'")

# input audio file
print(f"{Fore.LIGHTGREEN_EX}Audio file found. Loading audio file...")
clip = AudioSegment.from_file(f"Clone_Tests/Raw/{aud_file}.mp3", format="mp3")

# splitting audio file into chunks by segments lower than -60dB and longer than 5msec
print(f"{Fore.LIGHTGREEN_EX}Splitting into chunks...")
audio_chunks = split_on_silence(clip, min_silence_len=500, silence_thresh=-60)

# export all chunks
print(f"{Fore.LIGHTGREEN_EX}Exporting chunks...")
os.mkdir(f"Clone_Tests/Processed/{aud_file}")
count = 0
for segment in audio_chunks:
    output_file = f"Clone_Tests/Processed/{aud_file}/chunk_{count}.wav"
    segment.export(output_file, format="wav")
    count += 1
