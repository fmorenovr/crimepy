from .language_variables import lang_dict
import enchant
import numpy
from sklearn.metrics.pairwise import cosine_similarity

def cosine_sim(vecA, vecB):
    similarity = cosine_similarity([vecA], [vecB])
    similarity = similarity[0][0]
    return similarity

def initDistanceMatrix(token1, token2):
    distances = numpy.zeros((len(token1) + 1, len(token2) + 1))

    for t1 in range(len(token1) + 1):
        distances[t1][0] = t1

    for t2 in range(len(token2) + 1):
        distances[0][t2] = t2
    
    return distances
    

def levenshteinDistanceDP(token1, token2, log=False):
    distances = initDistanceMatrix(token1, token2)

    a = 0
    b = 0
    c = 0
    
    for t1 in range(1, len(token1) + 1):
        for t2 in range(1, len(token2) + 1):
            if (token1[t1-1] == token2[t2-1]):
                distances[t1][t2] = distances[t1 - 1][t2 - 1]
            else:
                a = distances[t1][t2 - 1]
                b = distances[t1 - 1][t2]
                c = distances[t1 - 1][t2 - 1]
                
                if (a <= b and a <= c):
                    distances[t1][t2] = a + 1
                elif (b <= a and b <= c):
                    distances[t1][t2] = b + 1
                else:
                    distances[t1][t2] = c + 1

    if log:
        printDistances(distances, len(token1), len(token2))
    
    return distances[len(token1)][len(token2)]

def printDistances(distances, token1Length, token2Length):
    for t1 in range(token1Length + 1):
        for t2 in range(token2Length + 1):
            print(int(distances[t1][t2]), end=" ")
        print()

def get_similar_word(word, language_to_eval="portuguese", log=False):
    d_lang = enchant.Dict(lang_dict[language_to_eval])
    suggest_list = d_lang.suggest(word)
    
    levenshtein_dict = {}
    for suggest_word in suggest_list:
        distance = levenshteinDistanceDP(suggest_word, word, log=log)
        levenshtein_dict[suggest_word] = distance
    
    closest_word = min(levenshtein_dict, key=levenshtein_dict.get)
    return closest_word, levenshtein_dict[closest_word], dict(sorted(levenshtein_dict.items(), key=lambda item: item[1]))
