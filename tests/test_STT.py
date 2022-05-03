import pytest
from ..CogNative.backend.modules.STT import STT

import sys

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

def compare_sentences(text1, text2):
    # Instantiate SentenceTransformer to compare sentence similarity
    model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

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
    if use_ST:
        assert get_accuracy(actual_text, text) > 0.9
    else:
        # Because bleu method won't work near as well
        assert get_accuracy(actual_text, text) > 0.5

    # Check if get_transcriptions() is storing the correct
    # correct text with the source audio file
    assert s.get_transcriptions()[example_path] == text

def test_spanish():
    """
    Audio obtained from Librivox.org
    https://librivox.org/angelina-por-rafael-delgado/

    Text obtained from:
    https://www.gutenberg.org/files/16082/16082-h/16082-h.htm#XXIII
    """
    s = STT()
    example_path = "tests/examples/AngelinaShort.wav"
    text = s.speech_to_text(example_path)

    actual_text = ("capítulo 23 de Angelina por Rafael Delgado "
                   "grabado para librivox.org por Karen Savage "
                   "capítulo 23 Grato pasatiempo diario fué para "
                   "mí la tertulia que se reunía todas las "
                   "tardes, dadas las cinco, en el despacho del "
                   "jurisconsulto. Concurrían de ordinario en "
                   "aquel sitio, el doctor Sarmiento a menos que "
                   "los deberes de su profesión se lo impidieran, "
                   "don Cosme Linares, y el escribano Quintín "
                   "Porras. Este era el alma de la tertulia por "
                   "lo bullicioso y decidor. Inteligente, "
                   "instruído, perspicaz, oportuno, hacía que le "
                   "oyéramos sin darnos cuenta de las horas que "
                   "pasaban. Recibió el título a mediados del 67; "
                   "había estudiado en Villaverde, en Pluviosilla "
                   "y en México. Leía mucho, y aunque joven, y "
                   "al parecer ligero, tenía grande afición a los "
                   "estudios serios")
    
    # Check if synthesized text vs actual text is greater than 90%
    if use_ST:
        assert get_accuracy(actual_text, text) > 0.9
    else:
        # Because bleu method won't work near as well
        assert get_accuracy(actual_text, text) > 0.5

def test_swedish():
    """
    Test STT with Swedish audio.

    Audio obtained from Librivox.org
    https://librivox.org/multilingual-short-works-collection-031-poetry-prose-by-various/

    Text obtained from:
    https://archive.org/details/samladeskrifter38stri/page/50/mode/2up
    """
    s = STT()
    example_path = "tests/examples/swedish.wav"
    text = s.speech_to_text(example_path)

    actual_text = ("Sista flyttningslasset hade gått; hyresgästen, "
                   "en ung man med sorgflor på hatten, vandrade "
                   "ännu en gång genom våningen för att se om han "
                   "glömt något. — Nej, han hade icke glömt något, "
                   "absolut ingenting; och så gick han ut, i "
                   "tamburen, fast besluten att icke mer tänka på "
                   "det han upplevat i denna våning. Men se, i "
                   "tamburen, invid telefonen, satt ett halvt ark "
                   "papper fastnubbat; och det var fullskrivet med "
                   "flera stilar, somt redigt med bläck, annat "
                   "klottrat med blyerts eller rödpenna.")
    
    # Check if synthesized text vs actual text is greater than 90%
    if use_ST:
        assert get_accuracy(actual_text, text) > 0.9
    else:
        # Because bleu method won't work near as well
        assert get_accuracy(actual_text, text) > 0.5
