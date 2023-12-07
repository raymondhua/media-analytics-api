from typing import Union

from fastapi import FastAPI
from fastapi.responses import Response
# from pydantic_settings import BaseSettings

# Imports the model_functions.py file
from model_functions import *

app = FastAPI()

yearFrom = 1970
yearTo = 2017
test = True

model_data = model_data(yearFrom, yearTo, test)

# @app.get("/")
# def read_root():
#     return {"Hello": "World"}

# class Settings(BaseSettings):
#     openapi_url: str = "/openapi.json"

@app.get("/words/{year}")
def top_words(year: int, breakID: Union[int, None] = 50):
    return model_data.top_words(year, breakID)

@app.get("/word/{year}")
def specific_word(year: int, words: str):
    return model_data.specific_word(year, words)

@app.get("/word/overtime/{word}")
def compare_overtime(word: str, yearfrom: Union[int, None] = yearFrom, yearto: Union[int, None] = yearTo):
    return model_data.compare_word_overtime(yearfrom, yearto, word)

@app.get("/similar/{year}/{wordToFind}")
def similar_words(year: int, wordToFind: str):
    return model_data.similar_words(year, wordToFind)

@app.get("/similarity/{year}")
def similarity_between_words(year: int, word1: str, word2: str):
    return model_data.similarity_between_words(year, word1, word2)

@app.get("/notmatch/{year}")
def not_match(year: int, words: str):
    return model_data.not_match(year, words)

@app.get("/xyz/{year}")
def analogies(year: int, x: str, y: str, z: str):
    positive = [y, z]
    negative = [x]
    return model_data.analogies(year, positive, negative)

@app.get("/tsne/{year}")
async def tsne(year: int, words: str):
    image = model_data.tsne(year, words)
    return Response(content=image, media_type="image/png")