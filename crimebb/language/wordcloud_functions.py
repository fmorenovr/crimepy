import matplotlib.pyplot as plt
import multidict as multidict
import nltk
import numpy as np
import re

from wordcloud import WordCloud, STOPWORDS

def getFrequencyDictForText(sentence):
    fullTermsDict = multidict.MultiDict()
    tmpDict = {}
    
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
