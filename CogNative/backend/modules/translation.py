from googletrans import Translator

from .languages import available_languages


class translation:
    def __init__(self):
        self.translator = Translator()

    def convert_language(self, lang):
        """This function ensures that the source language and
        destination language are supported by this module."""

        if lang not in available_languages.keys():
            raise (Exception("Please select a supported language."))

        return available_languages[lang]["translation"]

    def translate(self, text, src, dest):
        """This function requires both source and destination languages."""

        src = self.convert_language(src)
        dest = self.convert_language(dest)

        result = self.translator.translate(text, src=src, dest=dest)
        return result.text

    def translate_to(self, text, dest):
        """This function auto-detects the source language."""

        dest = self.convert_language(dest)

        result = self.translator.translate(text, dest=dest)
        return result.text

    def current_language(self, text):
        if len(text) > 500:
            return self.translator.detect(text[0:500]).lang
        else:
            return self.translator.detect(text).lang
