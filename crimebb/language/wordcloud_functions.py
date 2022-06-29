import matplotlib.pyplot as plt
import multidict as multidict
import nltk
import numpy as np
import re

from wordcloud import WordCloud, STOPWORDS

def getFrequencyDictForText(sentence, languages_to_eval=None):
    fullTermsDict = multidict.MultiDict()
    tmpDict = {}
    
    if language_to_eval is not None and len(language_to_eval)>=1:
        lang_stop = set()
        for language in language_to_eval:
            stopwords_set = set(stopwords.words(language))
            words_set = set(words)
            common_elements = words_set.intersection(stopwords_set)

            languages_ratios[language] = len(common_elements) # language "score"
            
    else:
        # Compute per language included in nltk number of unique stopwords appearing in analyzed text
        for language in stopwords.fileids():
            stopwords_set = set(stopwords.words(language))
            words_set = set(words)
            common_elements = words_set.intersection(stopwords_set)

            languages_ratios[language] = len(common_elements) # language "score"
    
    en_stop = set(nltk.corpus.stopwords.words("english"))
    ru_stop = set(nltk.corpus.stopwords.words("russian"))
    lang_stop = en_stop.union(ru_stop)

    # making dict for counting frequencies
    for text in sentence.split(" "):
        if re.match("a|the|an|the|to|in|for|of|or|by|with|is|on|that|be", text):
            continue
        if re.match("|".join(set(STOPWORDS)), text):
            continue
        if re.match("|".join(set(lang_stop)), text):
            continue
        
        val = tmpDict.get(text, 0)
        tmpDict[text.lower()] = val + 1
    for key in tmpDict:
        fullTermsDict.add(key, tmpDict[key])
    return fullTermsDict

def showWordCloud(text, mask=None, widht=1000, height=1000):

    x, y = np.ogrid[:widht, :height]

    if mask is None:
        mask = (x - widht/2) ** 2 + (y - widht/2) ** 2 > (widht/2) ** 2
        mask = 255 * mask.astype(int)

    wc = WordCloud(background_color="white", mask=mask, random_state=42)
    wc.generate_from_frequencies(text)

    fig = plt.subplots(figsize=(16,8))
    plt.axis("off")
    plt.imshow(wc, interpolation="bilinear")
    plt.show()
