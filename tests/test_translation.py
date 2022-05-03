import pytest
from ..CogNative.backend.modules.translation import translation

import sys
python_ver = sys.version
use_ST = False
if "3.7" in python_ver:
    # If Python 3.7, use sentence_transformers to evaluate sentences
    from sentence_transformers import SentenceTransformer, util
    use_ST = True
else:
    # Otherwise, we will use the bleu score (which is less accurate)
    from nltk.translate import bleu
    from nltk.translate.bleu_score import SmoothingFunction

def compare_sentences(text1, text2):
    """Compare sentences using ```sentence_transformers```. 
    This accounts for semantic meaning between words in sentences."""
    # Instantiate SentenceTransformer to compare sentence similarity
    model = SentenceTransformer('paraphrase-MiniLM-L12-v2')

    # Compute embedding for both lists
    actual_embeddings = model.encode(text1, convert_to_tensor=True)
    transcribed_embeddings = model.encode(text2, convert_to_tensor=True)

    # Compute cosine-similarities
    cosine_scores = util.pytorch_cos_sim(actual_embeddings, transcribed_embeddings)

    return cosine_scores.cpu().numpy()[0]

def get_accuracy(text1, text2):
    """Get accuracy with a supported method of sentence comparison.
    
    Python 3.7 will use ```sentence_transformers```, a neural network based
    approach to determine similarity between sentences. This method accounts
    for semantic meaning of words to compare similarity.

    Python > 3.7 will use the bleu method for comparing similarity
    between setences. This method does not account for semantics.
    """
    if use_ST:
        return compare_sentences(text1, text2)
    else:
        smoothie = SmoothingFunction().method4
        return bleu([text1], text2, smoothing_function=smoothie)

def test_invalid_src_language():
    src_lang = 'elvish' # Unsupported language
    dest_lang = 'english'

    english_text = ("The source language will be invalid")

    tr = translation()

    with pytest.raises(Exception):
        tr.translate(english_text, src_lang, dest_lang)


def test_invalid_dest_language():
    src_lang = 'english'
    dest_lang = 'klingon' # Unsupported language

    english_text = ("The destination language will be invalid.")

    tr = translation()

    with pytest.raises(Exception):
        tr.translate(english_text, src_lang, dest_lang)

def test_no_src_lang():
    dest_lang = 'spanish'

    english_text = ("The train arrives at Tarragona on time. "
                 "Pilar goes straight home but, as she "
                 "climbs the stairs she sees some strange "
                 "things: coloured balloons, red "
                 "heart-shaped cards, red roses.")

    spanish_text = ("El tren llega a Tarragona a su hora. "
                    "Pilar va directamente a casa, pero en "
                    "las escaleras, ve algunas cosas extrañas: "
                    "globos de colores, cartulinas rojas en "
                    "forma de corazón, rosas rojas.")

    tr = translation()
    translated_text = tr.translate_to(english_text, dest_lang)
    
    # Check if synthesized spanish_text vs translated_text
    # is greater than 80%
    if use_ST:
        get_accuracy(spanish_text, translated_text) > 0.8
    else:
        # Because bleu method won't work near as well
        assert get_accuracy(spanish_text, translated_text) > 0.5

def test_english_to_spanish():
    src_lang = 'english'
    dest_lang = 'spanish'

    english_text = ("The train arrives at Tarragona on time. "
                 "Pilar goes straight home but, as she "
                 "climbs the stairs she sees some strange "
                 "things: coloured balloons, red "
                 "heart-shaped cards, red roses.")

    spanish_text = ("El tren llega a Tarragona a su hora. "
                    "Pilar va directamente a casa, pero en "
                    "las escaleras, ve algunas cosas extrañas: "
                    "globos de colores, cartulinas rojas en "
                    "forma de corazón, rosas rojas.")

    tr = translation()
    translated_text = tr.translate(english_text, src_lang, dest_lang)
    
    # Check if synthesized spanish_text vs translated_text
    # is greater than 80%
    if use_ST:
        get_accuracy(spanish_text, translated_text) > 0.8
    else:
        # Because bleu method won't work near as well
        assert get_accuracy(spanish_text, translated_text) > 0.5

def test_spanish_to_english():
    src_lang = 'spanish'
    dest_lang = 'english'

    english_text = ("The train arrives at Tarragona on time. "
                 "Pilar goes straight home but, as she "
                 "climbs the stairs she sees some strange "
                 "things: coloured balloons, red "
                 "heart-shaped cards, red roses.")

    spanish_text = ("El tren llega a Tarragona a su hora. "
                    "Pilar va directamente a casa, pero en "
                    "las escaleras, ve algunas cosas extrañas: "
                    "globos de colores, cartulinas rojas en "
                    "forma de corazón, rosas rojas.")

    tr = translation()
    translated_text = tr.translate(spanish_text, src_lang, dest_lang)
    
    # Check if synthesized english_text vs translated_text
    # is greater than 80%
    if use_ST:
        get_accuracy(english_text, translated_text) > 0.8
    else:
        # Because bleu method won't work near as well
        assert get_accuracy(english_text, translated_text) > 0.5

def test_english_to_swedish():
    """
    Tests translation from English to Swedish.

    Parallel text obtained from:
    https://opus.nlpl.eu/CCMatrix/v1/en-sv_sample.html
    """
    dest_lang = 'swedish'

    english_text = ("No matter what he does, he must first know why "
                    "he is doing it, and then he must proceed with "
                    "his actions without having doubts or remorse "
                    "about them.”")

    swedish_text = ("Oavsett vad han gör måste han först veta "
                    "varför han gör det och då måste han fortsätta "
                    "med sina handlingar utan att ha tvivel eller "
                    "ånger om dem.")

    tr = translation()
    translated_text = tr.translate_to(english_text, dest_lang)
    
    # Check if synthesized swedish_text vs translated_text
    # is greater than 80%
    if use_ST:
        get_accuracy(swedish_text, translated_text) > 0.8
    else:
        # Because bleu method won't work near as well
        assert get_accuracy(swedish_text, translated_text) > 0.5
