from pathlib import Path
from shutil import rmtree
from pydub import AudioSegment
from pydub.silence import split_on_silence
from datetime import datetime

from ...models.RTVC.utils.printing import colorize

def optimize_split(audio_clip):
    print(
        colorize(
            f"Optimizing splitting thresholds...",
            "success",
        )
    )

    # take the first 3 minutes of the audio to determine
    # the best splitting thresholds
    duration = 180000 if len(audio_clip) > 180000 else len(audio_clip)
    audio_reduced = audio_clip[:duration]

    avg_chunk_sec = 0
    silence_len_thresh = 500
    max_decibels = -60

    # Make an initial split with the default thresholds
    audio_chunks = split_on_silence(
        audio_reduced, min_silence_len=silence_len_thresh, silence_thresh=max_decibels, keep_silence=silence_len_thresh/2
    )

    # Split audio based on a minimum silence length and
    # decibel threshold.
    # Average chunk length must be between 10 and 30 seconds in length
    while avg_chunk_sec < 10:
        print(
            colorize(
                f"Clips are too short ({avg_chunk_sec} seconds). Determing better thresholds...",
                "warning",
            )
        )
        silence_len_thresh += 250
        audio_chunks = split_on_silence(
            audio_reduced, min_silence_len=silence_len_thresh, silence_thresh=max_decibels, keep_silence=silence_len_thresh/2
        ) 

        # Calculate avg_chunk_sec length
        avg_chunk_sec = (len(audio_reduced) / 1000) / len(audio_chunks)

    while avg_chunk_sec > 30:
        print(
            colorize(
                f"Clips are too long ({avg_chunk_sec} seconds). Determing better thresholds...",
                "warning",
            )
        )
        if avg_chunk_sec < 10:
            # If the avg_chunk_sec length changed from greater than 30 seconds
            # to less than 10 seconds, we should not keep narrowing the search.
            continue
        silence_len_thresh -= 125
        audio_chunks = split_on_silence(
            audio_reduced, min_silence_len=silence_len_thresh, silence_thresh=max_decibels, keep_silence=silence_len_thresh/2
        )

        # Calculate avg_chunk_sec length
        avg_chunk_sec = (len(audio_reduced) / 1000) / len(audio_chunks)
    
    return silence_len_thresh

def split_chunk(chunk, min_silence_thresh):
    """Recursive function that ensures the individual audio chunks are less than 45 seconds."""
    max_decibels = -60
    split_chunks = split_on_silence(chunk, min_silence_len=min_silence_thresh, silence_thresh=max_decibels, keep_silence=min_silence_thresh/2)
    
    if min_silence_thresh < 250:
        print(colorize("There is no silence detectable in this audio file.", "error"))
        exit(1)

    # If any chunk in the split is greater than 45 seconds,
    # reduce the min_silence_len and try again.
    if not all(len(indiv_chunk) < 45000 for indiv_chunk in split_chunks):
        return split_chunk(chunk, min_silence_thresh-175)
    else:
        return split_chunks

def split_audio(audio_path, optimize=False):
    """Splits audio by silence."""
    file_check = Path(audio_path).exists()
    assert file_check, print(colorize(f"Audio file does not exist. ({audio_path})", "error"))

    # input audio file
    print(
        colorize(
            f"Audio file found ({audio_path}).",
            "success",
        )
    )
    clip = AudioSegment.from_file(audio_path, format="mp3")

    # Set default values
    silence_len_thresh = 500
    max_decibels = -60

    if optimize and clip.duration_seconds > 45:
        silence_len_thresh = optimize_split(clip)

    # Splitting the audio based on the default or the optimized
    # splitting thresholds for min silence length and max decibels
    print(colorize("Splitting into chunks...", "success"))
    audio_chunks_ini = split_on_silence(
        clip, min_silence_len=silence_len_thresh, silence_thresh=max_decibels, keep_silence=silence_len_thresh/2
    )

    audio_chunks = []
    extra = 0
    for chunk in audio_chunks_ini:
        # If the clip is too long, split into smaller clips
        if len(chunk) > 45000:
            # split_chunk ensures that chunks in split_smaller will be
            # less than 45 seconds
            split_smaller = split_chunk(chunk, silence_len_thresh)
            for smaller_chunk in split_smaller:
                if len(smaller_chunk) >= 1000:
                    extra += 1
                    audio_chunks.append(smaller_chunk)
            # break out of this loop
            continue
        
        # Add chunk to audio_chunks
        if len(chunk) >= 1000:
            audio_chunks.append(chunk)

    # remove directory if it already exists
    file_name_path = Path(audio_path).with_suffix("")
    if file_name_path.exists():
        rmtree(file_name_path)

    # create output directory
    file_name_path.mkdir()

    # export all chunks
    print(colorize("Exporting chunks...", "success"))
    split_output_paths = []
    for i, segment in enumerate(audio_chunks):
        output_file = f"{file_name_path}/chunk_{i}.wav"
        segment.export(output_file, format="wav")
        split_output_paths.append(output_file)

    print(colorize(f"Exported split audio to: {file_name_path}", "success"))

    return split_output_paths


if __name__ == "__main__":
    paths = split_audio("CogNative/examples/TCOC40.wav", optimize=True)
    for path in paths:
        print(path)
