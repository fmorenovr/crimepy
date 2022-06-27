import nltk

import pycountry
from collections import defaultdict
from heapq import nlargest
from nltk import wordpunct_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk.tokenize import word_tokenize, sent_tokenize
from string import punctuation

def classify_language(text):
    tc = nltk.classify.textcat.TextCat()
    guess_text = tc.guess_language(text)
    
    guess_language = pycountry.languages.get(alpha_3=guess_text).name
    return guess_language
    
def evaluate_text(texto, language_to_eval="portuguese"):
  sentencas = sent_tokenize(texto)
  palavras = word_tokenize(texto.lower())

  stopwords_pt = nltk.corpus.stopwords.words(language_to_eval)
  stopwords = set(stopwords_pt + list(punctuation))
  palavras_sem_stopwords = [palavra for palavra in palavras if palavra not in stopwords]

  frequencia = FreqDist(palavras_sem_stopwords)

  sentencas_importantes = defaultdict(int)

  for i, sentenca in enumerate(sentencas):
      for palavra in word_tokenize(sentenca.lower()):
          if palavra in frequencia:
              sentencas_importantes[i] += frequencia[palavra]

  idx_sentencas_importantes = nlargest(4, sentencas_importantes, sentencas_importantes.get)

#  for i in sorted(idx_sentencas_importantes):
#    print(sentencas[i])
    
  return frequencia, idx_sentencas_importantes, sentencas

#----------------------------------------------------------------------
def _calculate_languages_ratios(text, language_to_eval=None):
    languages_ratios = {}

    tokens = wordpunct_tokenize(text)
    words = [word.lower() for word in tokens]

    if language_to_eval is not None and len(language_to_eval)>=1:
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

    return languages_ratios
    
#----------------------------------------------------------------------
def detect_language(text, language_to_eval=None):
    ratios = _calculate_languages_ratios(text, language_to_eval=language_to_eval)
    return ratios
    #most_rated_language = max(ratios, key=ratios.get)
    #return most_rated_language
