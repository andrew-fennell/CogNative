import sys
from googletrans import Translator

sys.path.append("../")
from languages import available_languages


class translation:
    def __init__(self):
        self.translator = Translator()

    def convert_language(self, lang):
        """This function ensures that the source language and
        destination language are supported by this module."""

        if lang not in available_languages.keys():
            raise (Exception("Please select a supported language."))

        return available_languages[lang]["translation"]

    def translate(self, text, src, des):
        """This function requires both source and destination languages."""

        src = self.convert_language(src)
        des = self.convert_language(des)

        result = self.translator.translate(text, src=src, dest=des)
        return result.text

    def translate_to(self, text, des):
        """This function auto-detects the source language."""

        des = self.convert_language(des)

        result = self.translator.translate(text, dest=des)
        return result.text
