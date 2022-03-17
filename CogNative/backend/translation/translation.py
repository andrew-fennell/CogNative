from googletrans import Translator


class translation:

    def __int__(self):
        self.translator = Translator()

    def translate(self, text, src, des):
        result = self.translator.translate(text, src=src, dest=des)
        return result.text

    def translate_to(self, text, des):
        result = self.translator.translate(text, dest=des)
        return result.text
