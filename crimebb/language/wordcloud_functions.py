import matplotlib.pyplot as plt
import multidict as multidict
import nltk
import numpy as np
import re
from nltk.corpus import stopwords

import wordcloud
from wordcloud import WordCloud

def getFrequencyDictForText(sentence, language_to_eval=None):
    fullTermsDict = multidict.MultiDict()
    tmpDict = {}
    lang_stop = set()
    
    if language_to_eval is not None and len(language_to_eval)>=1:
        for language in language_to_eval:
            current_lang = set(stopwords.words(language))
            lang_stop.union(current_lang)
            
    else:
        # Compute per language included in nltk number of unique stopwords appearing in analyzed text
        for language in stopwords.fileids():
            current_lang = set(stopwords.words(language))
            lang_stop.union(current_lang)

    # carateres speciais
    #regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
    # removing some characters
    #sentence = re.sub('[@_!#$%^&*,;()<>?/\|\[\]}{~:=]', " ", sentence)
    #sentence = sentence.replace("http", " ")
    #sentence = sentence.replace("https", " ")
    # making dict for counting frequencies
    for text in sentence.split(" "):
        if len(text)==0:
            continue
        
        if re.match("|".join(set(wordcloud.STOPWORDS).union(set(lang_stop))), text):
            continue
        
        val = tmpDict.get(text, 0)
        tmpDict[text.lower()] = val + 1
    for key in tmpDict:
        fullTermsDict.add(key, tmpDict[key])
    return fullTermsDict

def showWordCloud(text, mask=None, widht=1000, height=1000, figsize=(20,10)):

    x, y = np.ogrid[:widht, :height]

    if mask is None:
        mask = (x - widht/2) ** 2 + (y - widht/2) ** 2 > (widht/2) ** 2
        mask = 255 * mask.astype(int)

    wc = WordCloud(background_color="white", max_words=1000, mask=mask, random_state=42)
    wc.generate_from_frequencies(text)

    fig = plt.subplots(figsize=figsize)
    plt.axis("off")
    plt.imshow(wc, interpolation="bilinear")
    plt.show()
