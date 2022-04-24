import pytest
from ....CogNative.backend.modules.translation import translation

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

english_text1 = ("The train arrives at Tarragona on time. "
                 "Pilar goes straight home but, as she "
                 "climbs the stairs she sees some strange "
                 "things: coloured balloons, red "
                 "heart-shaped cards, red roses.")

spanish_text1 = ("El tren llega a Tarragona a su hora. "
                 "Pilar va directamente a casa, pero en "
                 "las escaleras, ve algunas cosas extrañas: "
                 "globos de colores, cartulinas rojas en "
                 "forma de corazón, rosas rojas.")

english_text2 = ("Everyone has the right freely to participate in the cultural life of the community, to enjoy the arts and to share in scientific advancement and its benefits.")

swedish_text2 = ("Envar har rätt att fritt taga del i samhällets kulturella liv, att njuta av konsten samt att bli delaktig av vetenskapens framsteg och dess förmåner.")

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

    tr = translation()

    with pytest.raises(Exception):
        translated_text = tr.translate(english_text1, src_lang, dest_lang)


def test_invalid_dest_language():
    src_lang = 'english'
    dest_lang = 'klingon' # Unsupported language

    tr = translation()

    with pytest.raises(Exception):
        translated_text = tr.translate(english_text1, src_lang, dest_lang)

def test_no_src_lang():
    dest_lang = 'spanish'

    tr = translation()
    translated_text = tr.translate_to(english_text1, dest_lang)
    
    # Check if synthesized spanish_text vs translated_text 
    # is greater than 70%
    assert get_accuracy(spanish_text1, translated_text) > 0.7

def test_english_to_spanish():
    src_lang = 'english'
    dest_lang = 'spanish'

    tr = translation()
    translated_text = tr.translate(english_text1, src_lang, dest_lang)
    
    # Check if synthesized spanish_text vs translated_text 
    # is greater than 70%
    assert get_accuracy(spanish_text1, translated_text) > 0.7

def test_spanish_to_english():
    src_lang = 'spanish'
    dest_lang = 'english'

    tr = translation()
    translated_text = tr.translate(spanish_text1, src_lang, dest_lang)
    
    # Check if synthesized spanish_text vs translated_text 
    # is greater than 70%
    assert get_accuracy(english_text1, translated_text) > 0.7
