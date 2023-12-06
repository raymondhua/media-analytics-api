# from typing import Union

from fastapi import FastAPI

# Imports the loadModels.py and cleanInput.py files
from modelFunctions import *

app = FastAPI()

# @app.get("/")
# def read_root():
#     return {"Hello": "World"}

# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}

@app.get("/words/{year}/{breakID}")
def topWords(year: int, breakID: int):
    return top_words(year, breakID)

@app.get("/similar/{year}/{wordToFind}")
def similarWords(year: int, wordToFind: str):
    return similar_words(year, wordToFind)

@app.get("/similar/{year}")
def similarity(year: int, word1: str, word2: str):
    return similarity_between_words(year, word1, word2)