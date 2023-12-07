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

class model_data:

    def top_words(self, year, breakID):
        #Opens the model from the loadModels.py
        model = openModel(year)
        word_vectors = model.wv.index_to_key
        # Gets the length of the model
        model_length = len(word_vectors)
        word_dict = {}
        # Gets all the words from the model and stores in the dictionary
        for word in word_vectors:
            word_dict[word] = model.wv.get_vecattr(word, "count")/model_length
        # Sorts the words by the least frequent words and reverses
        topWords = sorted(word_dict.items(), key=lambda kv: kv[1], reverse=True)
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
    def similar_words(self, year, wordToFind):
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
    def similarity_between_words(self, year, word1, word2):
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

    # Function that returns a dictionary which certain words are the odd one out
    def not_match(self, year, wordString):
        # Initializes the data dictionary with one key, notMatch initialized to empty list
        data = {}
        data['notMatch'] = []
        # Opens the model from the loadModels.py with the year passing in
        model = openModel(year)
        # Converts the string into a list
        wordArray = convertToList(wordString)
        try:
            # Runs the Gensim function similarity with the word array passing in
            # And returns the which word is the odd one out in the array
            notMatch =  model.wv.doesnt_match(wordArray)
            # Appends the notMatch list with the rate stored in the key called similarity
            data['notMatch'].append({'request': wordString, 'word' : notMatch})
        except:
            # Appends the notMatch list with not found passed in the key word
            data['notMatch'].append({'request': wordString, 'word' : "Not found"})
        return data
    
    # Function that returns a dictionary which contains information about a specific word
    def specific_word(self, year, wordString):
        # Initializes the data dictionary with one key, word initialized to empty list
        data = {}
        data['word'] = []
        # Opens the model from the loadModels.py with the year passing in
        wordArray = convertToList(wordString)
        for word in wordArray:
            self.get_word_info(year, word, data['word'])
        data['code'] = 1
        return data
    
    def get_word_info(self, year, word, wordDict):
        def append_data(year, word, rank, count, frequency):
            wordDict.append({
            'year': int(year),
            'word': word,
            'rank': int(rank),
            'count': int(count),
            'frequency': frequency
        })
        model = openModel(year)
        # Sets the total word count to 0
        totalWordCount = 0
        # Cleans the word and stores it into wordInput
        wordInput = cleanInput(word)
        # Adds all the word counts in the model
        for w in model.wv.index_to_key:
            totalWordCount += model.wv.get_vecattr(w, "count")
        try:
            # Returns the word count in the model for that certain word
            wordCount = model.wv.get_vecattr(wordInput, "count")
            # Divides the word count by the total word count and divide it by 100
            wordFreq = (wordCount/totalWordCount) * 100
            # Appends the data into 
            # data['word'] = list
            # year = year of the model
            # model.wv.key_to_index[wordInput] + 1 = ranking
            # wordCount = word count in the model for that certain word
            # wordFreq = Frequency of the word in the model
            append_data(year, word, model.wv.key_to_index[wordInput] + 1, wordCount, wordFreq)
        # If the try handling throws an error, it would return the ranking, count, and frequency to 0
        except:
            append_data(year, word, 0, 0, 0)
        return wordDict
        
    # Function that returns information of a specific word between two years
    def compare_word_across_years(self, yearFrom, yearTo, word):
        # Initializes the data dictionary with one key, word initialized to empty list
        data = {}
        # If the yearFrom is less than yearTo it would run the function below
        if yearFrom > yearTo:
            yearFrom, yearTo = yearTo, yearFrom
        data['word'] = []
        # Cleans the word and stores it into wordInput
        wordInput = cleanInput(word)
        # For loop function that runs from the year the yearFrom until yearTo
        for x in range(yearFrom, yearTo+1):
            self.get_word_info(x, word, data['word'])
        data['code'] = 1
        return data
    
    # Function that returns analogies of a an array given
    # Positive and negative are arrays
    def analogies(self, year, positive, negative):
        # Initializes the data dictionary with one key, similarWords initialized to empty list
        data = {}
        data['similarWords'] = []
        # Opens the model from the loadModels.py with the year passing in
        model = openModel(year)
        # Cleans the arrays
        positiveInput = lowerArray(positive)
        negativeInput = lowerArray(negative)
        try: 
            # Runs the Gensim function similarity with the positives and negatives passing in
            # And returns the which word is the most similar words
            similarWordArray = model.wv.most_similar(positive=positiveInput, negative=negativeInput)
            # Runs the for function with x being the word(key) and y being the frequency rate (y)
            data['similarWords'].append({'x': negative[0], 'y': positive[0], 'z': positive[1], 'word': similarWordArray[0][0]})
        except:
            data['similarWords'].append({'x': negative[0], 'y': positive[0], 'z': positive[1], 'word': "Word(s) not found"})
        return data
    
    def generate_tsne_graph(self, model, items):
        def makeTSNEDict(items):
            d = {}
            for item in items:
                try: 
                    d[item] = model.wv.key_to_index[item]
                except:
                    print("Word not found")
            return d
        d = makeTSNEDict(items)
        vocab = list(d)
        X = model.wv[vocab]
        p = 5
        tsne = TSNE(perplexity=p, n_components=2, learning_rate=5, init='pca',random_state=3, n_iter=150000)
        X_tsne = tsne.fit_transform(X)
        df = pd.concat([pd.DataFrame(X_tsne), pd.Series(vocab)], axis=1)
        df.columns = ['x', 'y', 'word']
        return df
    
    def tsne(self, year, words):
        # Talk to David about this function
        def generate_tsne_Image(model, items):
            tsne_df = self.generate_tsne_graph(model, items)

            fig = plt.figure()
            ax = fig.add_subplot(1, 1, 1)
            ax.scatter(tsne_df['x'], tsne_df['y'])

            for i, txt in enumerate(tsne_df['word']):
                ax.annotate(txt, (tsne_df['x'].iloc[i], tsne_df['y'].iloc[i]))
 
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            plt.close(fig)
            return buf.getvalue()
        
        model = openModel(year)
        items = convertToList(words)
        
        return generate_tsne_Image(model, items)