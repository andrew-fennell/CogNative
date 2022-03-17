from googletrans import Translator


class translation:

    def __init__(self):
        self.translator = Translator()

    # this function requires both source and destination languages
    def translate(self, text, src, des):
        result = self.translator.translate(text, src=src, dest=des)
        return result.text

    # this function auto-detects the source language
    def translate_to(self, text, des):
        result = self.translator.translate(text, dest=des)
        return result.text
