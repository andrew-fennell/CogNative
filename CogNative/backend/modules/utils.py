from pathlib import Path
from pydub import AudioSegment

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


if __name__ == "__main__":
    audio_path = input("Name of mp3 audio file:\n")
    assert Path(audio_path).exists, print(
        colorize(f"File does not exist. ({audio_path})", "error")
    )
    print(colorize(f"Exported to: {mp3_to_wav(audio_path)}", "success"))
