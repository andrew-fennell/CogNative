import pytest
from ....CogNative.backend.modules.STT import STT

import os
import sys
import logging

python_ver = sys.version
use_ST = False
if "3.7" in python_ver:
    # If Python 3.7, use sentence_transformers to evaluate sentences
    # Otherwise, we will use the bleu score (which is less accurate)
    from sentence_transformers import SentenceTransformer, util
    use_ST = True
else:
    from nltk.translate import bleu
    from nltk.translate.bleu_score import SmoothingFunction

def test_invalid_language():
    """Need to input audio with a language that is not supported."""
    pass

def compare_sentences(text1, text2):
    # Instantiate SentenceTransformer to compare sentence similarity
    model = SentenceTransformer('paraphrase-MiniLM-L12-v2')

    # Compute embedding for both lists
    actual_embeddings = model.encode(text1, convert_to_tensor=True)
    transcribed_embeddings = model.encode(text2, convert_to_tensor=True)

    # Compute cosine-similarities
    cosine_scores = util.pytorch_cos_sim(actual_embeddings, transcribed_embeddings)

    return cosine_scores.cpu().numpy()[0]

def get_accuracy(text1, text2):
    if use_ST:
        return compare_sentences(text1, text2)
    else:
        smoothie = SmoothingFunction().method4
        return bleu([text1], text2, smoothing_function=smoothie)

def test_english():
    s = STT()
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
    assert get_accuracy(actual_text, text) > 0.9

    example_path2 = "tests/examples/DavidHowell15.wav"
    text2 = s.speech_to_text(example_path2)

    actual_text2 = ("Once upon a time, in a place not far "
                    "from where you're standing, there lived"
                    " a community of farmers merchants "
                    "blacksmiths strong women, and a few others"
                    " who used the resources they had "
                    "available to make life work.")
    
    # Check if synthesized text vs actual text is greater than 90%
    assert get_accuracy(actual_text2, text2) > 0.9

    # Check if get_transcriptions() is storing the correct
    # correct text with the source audio file
    assert s.get_transcriptions()[example_path] == text
    assert s.get_transcriptions()[example_path2] == text2
