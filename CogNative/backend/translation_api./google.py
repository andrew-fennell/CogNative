from googletrans import Translator

translator = Translator()
result = translator.translate('this is a beautiful world. One that we '
                              'hardly appreciate!', src='en', dest='es')

print(result.src)
print(result.dest)
print(result.text)
