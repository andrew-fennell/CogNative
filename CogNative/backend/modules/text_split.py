import re

def split_text(text):
    # SEPARATE TEXT BY PUNCTUATION
    punctuation_regex = '\. |\? |\! |\; |\: | \— |\—|\.\.\. |\.|\?|\!|\;|\:|\.\.\.'
    punctuation = re.findall(punctuation_regex, text)
    input_subs_split = re.split(punctuation_regex, text)
    input_subs_split.pop()

    # JOIN SENTENCES TO BE TOGETHER
    input_subs = []
    for i in range(0, len(input_subs_split)):
        input_subs.append(input_subs_split[i] + punctuation[i])
    return input_subs