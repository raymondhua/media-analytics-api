# Load Models file
# Only include functions that are related to opening/retrieving the models
import os.path
import os
from gensim.models import Word2Vec

class Models:
    def __init__(self, yearStart, yearEnd, test=False):
        self.yearStart = yearStart
        self.yearEnd = yearEnd
        self.models = {}
        if test:
            self.models = self.loadTestModels()
        else:
            self.models = self.loadAllModels()

    # Function that loads all models
    def loadAllModels(self):
        # folder path hardcoded for the live server, if it doesn't run properly ask the Ops team
        folderPath = "/home/huara883/models"
        # If the operating system is a Windows machine, it would get the folder path of this repo and
        if os.name == 'nt':
            folderPath = "D:\\Media-Analytics-Models"
        for x in range(self.yearStart, self.yearEnd+1):
            # David doesn't have a model for 1980, so if x is 1980 it would use the 1979 model for that year
            if x != 1980:    
                self.models[str(x)] = Word2Vec.load(folderPath + "/" + str(x))
            else:
                self.models[str(x)] = self.models[str(x-1)]
        return self.models

    # Function that opens a model
    def openModel(self, year):
        # Retrieves the model for the year
        return self.models[str(year)]

    # Function that loads test models
    def loadTestModels(self):
        # You can add more words to the array
        sentences = [['first', 'sentence'], ['second', 'sentence'], ['being', 'well'], ['trump', 'clinton'], ['obama', 'clinton'], ['trump', 'clinton', 'obama', 'clinton'], ['hard', 'leaver']]
        for x in range(self.yearStart, self.yearEnd+1):    
            self.models[str(x)] = Word2Vec(sentences, min_count=1)
        return self.models