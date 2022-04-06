import pytest
from ....CogNative.backend.modules.translation import translation

from nltk.translate import bleu
from nltk.translate.bleu_score import SmoothingFunction

english_text = ("Once there was a man who had a wife "
    "and a young daughter. He loved his wife and "
    "daughter dearly, for they were both kind and "
    "loving. Sadly, his wife died before she was "
    "thirty years old. Soon the man decided to "
    "marry again. But his new wife was not kind "
    "like the first, but proud and quite cruel. "
    "She also had two daughters, who were just "
    "like her. She did not like her new "
    "step-daughter at all, who was much kinder "
    "and prettier than herself and her daughters. "
    "So the poor girl was given the dirtiest work "
    "in the house. She had to scrub dishes and "
    "floors, clean out fireplaces—just like a "
    "servant might have done. Her sisters were "
    "given fine rooms to sleep in, while she was "
    "given only a small, cold room in the attic. "
    "Her bed was made of straw.")

spanish_text = ("Había una vez un hombre que "
    "tenía una esposa y una hija pequeña. "
    "Quería mucho a su mujer y a su hija, "
    "porque ambas eran amables y cariñosas. "
    "Lamentablemente, su mujer murió antes "
    "de cumplir los treinta años. Pronto el "
    "hombre decidió casarse de nuevo. Pero "
    "su nueva esposa no era amable como la "
    "primera, sino orgullosa y bastante cruel. "
    "También tenía dos hijas, que eran como "
    "ella. No le gustaba nada su nueva "
    "hijastra, que era mucho más amable y bonita "
    "que ella y sus hijas. Así que a la pobre "
    "chica le dieron el trabajo más sucio de "
    "la casa. Tuvo que fregar los platos y los "
    "suelos, limpiar las chimeneas... como si "
    "fuera una criada. A sus hermanas les dieron "
    "buenas habitaciones para dormir, mientras "
    "que a ella sólo le dieron una pequeña y "
    "fría habitación en el ático. Su cama era "
    "de paja.")

def test_invalid_src_language():
    src_lang = 'elvish' # Unsupported language
    dest_lang = 'english'

    tr = translation()

    with pytest.raises(Exception):
        translated_text = tr.translate(english_text, src_lang, dest_lang)


def test_invalid_dest_language():
    src_lang = 'english'
    dest_lang = 'klingon' # Unsupported language

    tr = translation()

    with pytest.raises(Exception):
        translated_text = tr.translate(english_text, src_lang, dest_lang)

def test_no_src_lang():
    dest_lang = 'spanish'

    tr = translation()
    translated_text = tr.translate_to(english_text, dest_lang)
    
    # Check if synthesized spanish_text vs translated_text 
    # is greater than 80%
    smoothie = SmoothingFunction().method4
    assert bleu([spanish_text], translated_text,
                smoothing_function=smoothie) > 0.7

def test_english_to_spanish():
    src_lang = 'english'
    dest_lang = 'spanish'

    tr = translation()
    translated_text = tr.translate(english_text, src_lang, dest_lang)
    
    # Check if synthesized spanish_text vs translated_text 
    # is greater than 80%
    smoothie = SmoothingFunction().method4
    assert bleu([spanish_text], translated_text,
                smoothing_function=smoothie) > 0.7

def test_spanish_to_english():
    src_lang = 'spanish'
    dest_lang = 'english'

    tr = translation()
    translated_text = tr.translate(spanish_text, src_lang, dest_lang)
    
    # Check if synthesized spanish_text vs translated_text 
    # is greater than 80%
    smoothie = SmoothingFunction().method4
    assert bleu([english_text], translated_text,
                smoothing_function=smoothie) > 0.7
