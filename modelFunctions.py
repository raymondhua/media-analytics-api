# https://radimrehurek.com/gensim/models/keyedvectors.html
from gensim.models import Word2Vec
import pandas as pd
from sklearn.manifold import TSNE

# Imports the loadModels.py and cleanInput.py files
from loadModels import *
from cleanInput import *

import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import io
import decimal

def top_words(year, breakID):
    #Opens the model from the loadModels.py
    model = openModel(year)
    wordVectors = model.wv.index_to_key
    # Gets the length of the model
    modelLength = len(wordVectors)
    wordDict = {}
    # Gets all the words from the model and stores in the dictionary
    for word in wordVectors:
        wordDict[word] = model.wv.get_vecattr(word, "count")/modelLength
    # Sorts the words by the least frequent words and reverses
    topWords = sorted(wordDict.items(), key=lambda kv: kv[1], reverse=True)
    # Sets the count as 1
    count = 1
    #
    data = {}
    data['topWords'] = []
    for x, y in topWords:
        if not x.isdigit():
            data['topWords'].append({'word': x, 'rank':count, 'frequently': y})
            # If the breakID equal to the count then it breaks the for loop
            if count == breakID:
                break
            # Increments the count by 1
            count += 1
    # Returns the data dictionary
    return data

# Function that returns a dictionary of similar words for a certain word
def similar_words(year, wordToFind):
    # Initializes the data dictionary with one key, similarWords initialized to empty list
    data = {}
    data['similarWords'] = []
    # Opens the model from the loadModels.py with the year passing in
    model = openModel(year)
    # Runs the try and exceptions method
    try:
        # Runs the Gensim function most_similar with the wordToFind function passing in (should return at least 10 words)
        similarWordArray = model.wv.most_similar(cleanInput(wordToFind))
        # x stands for word (key)
        # y stands for frequent number (value)
        for x, y in similarWordArray: 
            data['similarWords'].append({'word': x, 'frequently': y})
    # If any errors were thrown it returns the frequency as not found
    except:
        data['similarWords'].append({'word': wordToFind, 'frequently': "Not found"})
    # Returns the data dictionary
    return data

# Function that returns a dictionary of two similar words
def similarity_between_words(year, word1, word2):
    # Initializes the data dictionary with one key, similarity initialized to empty list
    data = {}
    data['similarity'] = []
    # Opens the model from the loadModels.py with the year passing in
    model = openModel(year)
    # Cleans the word inputs and stores them into wordInput1 and wordInput2
    wordInput1 = cleanInput(word1)
    wordInput2 = cleanInput(word2)
    try:
        # Runs the Gensim function similarity with the wordInput1 and wordInput2 function passing in
        # And should return the frequent rate between the two words
        similar = model.wv.similarity(wordInput1, wordInput2)
        # Appends the similarity list with the rate stored in the key called similarity
        data['similarity'].append({'similarity': format(similar, ".15g"), 'word1': word1, 'word2': word2})
    # If it doesn't returns a frequent rate it returns not found
    except:
        data['similarity'].append({'similarity': "Not found", 'word1': word1, 'word2': word2})
    return data