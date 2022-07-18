import nltk
from nltk import wordpunct_tokenize
from nltk.probability import FreqDist
from nltk.tokenize import word_tokenize, sent_tokenize
from string import punctuation, digits

from .language_variables import lang_dict

import enchant

def get_words_ratio(freq_dict, language_to_eval="portuguese"):
    lang_d = enchant.Dict(lang_dict[language_to_eval])
    total_ = len(freq_dict)
    relative_ = 0
    incorrect_words = []
    correct_words = []
    
    for word in freq_dict.keys():
        if lang_d.check(word):
            relative_ +=1
            correct_words.append(word)
        else:
            incorrect_words.append(word)
    
    try:
        return relative_/total_, incorrect_words, correct_words
    except: # error divided by 0
        return 0, incorrect_words, correct_words

def get_words_frequency(texto, language_to_eval=None, keep_punct=True):
    if language_to_eval is not None:
        #Tokenizing by characters/words
        palavras_inside = word_tokenize(texto.lower(), language=language_to_eval) if keep_punct else wordpunct_tokenize(texto.lower())

        # Getting StopWords for the language
        stopwords_pt = nltk.corpus.stopwords.words(language_to_eval)
        # avoid numbers (alone) punctuations and stopwords
        stopwords_avoid = set(stopwords_pt).union(set(punctuation)).union(set(digits))
        palavras_sem_stopwords = [palavra for palavra in palavras_inside if palavra not in stopwords_avoid]

    else:
        palavras_inside = word_tokenize(texto.lower())
        stopwords_avoid = set(punctuation).union(set(digits))
        palavras_sem_stopwords = [palavra for palavra in palavras_inside if palavra not in stopwords_avoid]
    # making the frequency dict
    frequencia = FreqDist(palavras_sem_stopwords)

    return frequencia

def get_language_score(text, language_to_eval=None, keep_punct=True):
    languages_ratios = {}
    
    if language_to_eval is None:
        language_to_eval = nltk.corpus.stopwords.fileids()
    
    for language in language_to_eval:
        languages_ratios[language] = {}
        freq_lang = get_words_frequency(text, language, keep_punct=keep_punct)
        ratio_lang, incorrect_words_lang, correct_words_lang = get_words_ratio(freq_lang, language)
        
        languages_ratios[language]["ratio"] = ratio_lang
        languages_ratios[language]["incorrect_words"] = incorrect_words_lang
        languages_ratios[language]["correct_words"] = correct_words_lang
    
    return languages_ratios
    
def detect_language_and_words(text, language_to_eval=None, keep_punct=True):
    lang_freq = get_language_score(text, language_to_eval=language_to_eval, keep_punct=keep_punct)
    ratios = {}
    incorrect_words = {}
    correct_words = {}
    for lang in language_to_eval:
      ratios[lang] = lang_freq[lang]["ratio"]
      incorrect_words[lang] = lang_freq[lang]["incorrect_words"]
      correct_words[lang] = lang_freq[lang]["correct_words"]
    
    return ratios, incorrect_words, correct_words
    
def detect_language(text, language_to_eval=None, keep_punct=True):
    lang_freq = get_language_score(text, language_to_eval=language_to_eval, keep_punct=keep_punct)
    ratios = {}
    for lang in language_to_eval:
      ratios[lang] = lang_freq[lang]["ratio"]
    
    return ratios
    #most_rated_language = max(ratios, key=ratios.get)
    #return most_rated_language

def get_incorrect_words(text, language_to_eval=None, keep_punct=True):
    lang_freq = get_language_score(text, language_to_eval=language_to_eval, keep_punct=keep_punct)
    incorrect_words = {}
    for lang in language_to_eval:
      incorrect_words[lang] = lang_freq[lang]["incorrect_words"]
    
    return incorrect_words

def get_correct_words(text, language_to_eval=None, keep_punct=True):
    lang_freq = get_language_score(text, language_to_eval=language_to_eval, keep_punct=keep_punct)
    correct_words = {}
    for lang in language_to_eval:
      correct_words[lang] = lang_freq[lang]["correct_words"]
    
    return correct_words
    
# NOT USED
#----------------------------------------------------------------------
def __calculate_languages_ratios(text, language_to_eval=None):
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
    
