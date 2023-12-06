# Load Models file
# Only include functions that are related to opening/retrieving the models
import os.path
import os
from gensim.models import Word2Vec

# If David has models that are not within the range you can change it here
yearStart = 1970
yearEnd = 2017

# Function that loads all models
def loadAllModels():
    models = {}
    # folder path hardcoded for the live server, if it doesn't run properly ask the Ops team
    folderPath = "/home/huara883/models"
    # If the operating system is a Windows machine, it would get the folder path of this repo and
    if os.name == 'nt':
        folderPath = "D:\\Media-Analytics-Models"
    for x in range(yearStart, yearEnd+1):
        # David doesn't have a model for 1980, so if x is 1980 it would use the 1979 model for that year
        if x != 1980:    
            models[str(x)] = Word2Vec.load(folderPath + "/" + str(x))
        else:
            models[str(x)] = models[str(x-1)]
    return models

# Function that opens a model
def openModel(year):
    # Retrieves the model for the year
    return modelsDict[str(year)]

# Function that loads test models
def loadTestModels():
    # You can add more words to the array
    sentences = [['first', 'sentence'], ['second', 'sentence'], ['being', 'well'], ['trump', 'clinton'], ['obama', 'clinton'], ['trump', 'clinton', 'obama', 'clinton'], ['hard', 'leaver']]
    models = {}
    for x in range(yearStart, yearEnd+1):    
        models[str(x)] = Word2Vec(sentences, min_count=1)
    return models

# modelsDict would load all models from 1975 to 2017
# This will take some time to load because of how big they are and uses too much memory
# If you want to run the test models with less memory usage replace loadAllModels with loadTestModels
modelsDict = loadTestModels()