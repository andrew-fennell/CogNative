import pytest
from ....CogNative.backend.modules.STT import STT

from nltk.translate import bleu
from nltk.translate.bleu_score import SmoothingFunction


def test_invalid_language():
    with pytest.raises(Exception):
        s = STT(source_language="randomness")

def test_english():
    s = STT(source_language="english")
    example_path = "tests/examples/BillMaher22.wav"
    text = s.speech_to_text(example_path)

    actual_text = ("It wasn't really necessary. I tried to "
                   "explain one night on my show that I "
                   "think a lot of this comes from he thinks"
                   " he's the savior of the Russian people. I"
                   " think, when you get to that level where "
                   "he's been in office, he's been an absolute"
                   " power for 20 years. Um, what is left what "
                   "you know what's in the soul of a man? He "
                   "wants to be a hero and he thinks this is "
                   "the way to do it I think people know, "
                   "this is history major stuff.")
    
    # Check if synthesized text vs actual text is greater than 90%
    smoothie = SmoothingFunction().method4
    assert bleu([actual_text], text, smoothing_function=smoothie) > 0.9

    example_path2 = "tests/examples/DavidHowell15.wav"
    text2 = s.speech_to_text(example_path2)

    actual_text2 = ("Once upon a time, in a place not far "
                    "from where you're standing, there lived"
                    " a community of farmers merchants "
                    "blacksmiths strong women, and a few others"
                    " who used the resources they had "
                    "available to make life work.")
    
    # Check if synthesized text vs actual text is greater than 90%
    assert bleu([actual_text2], text2, smoothing_function=smoothie) > 0.9

    # Check if get_transcriptions() is storing the correct
    # correct text with the source audio file
    assert s.get_transcriptions()[example_path] == text
    assert s.get_transcriptions()[example_path2] == text2
