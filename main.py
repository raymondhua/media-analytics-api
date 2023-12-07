# from typing import Union

from fastapi import FastAPI
from fastapi.responses import Response
from pydantic_settings import BaseSettings

# Imports the loadModels.py and cleanInput.py files
from model_functions import *

app = FastAPI()

model_data = model_data()

# @app.get("/")
# def read_root():
#     return {"Hello": "World"}

# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}
# class Settings(BaseSettings):
#     openapi_url: str = "/openapi.json"

@app.get("/words/{year}/{breakID}")
def top_words(year: int, breakID: int):
    return model_data.top_words(year, breakID)

@app.get("/word/{year}")
def specific_word(year: int, words: str):
    return model_data.specific_word(year, words)

@app.get("/similar/{year}/{wordToFind}")
def similar_words(year: int, wordToFind: str):
    return model_data.similar_words(year, wordToFind)

@app.get("/similarity/{year}")
def similarity_between_words(year: int, word1: str, word2: str):
    return model_data.similarity_between_words(year, word1, word2)

@app.get("/notmatch/{year}")
def not_match(year: int, words: str):
    return model_data.not_match(year, words)

@app.get("/compare/{word}")
def compare(word: str, year_from: int, year_to: int):
    return model_data.compare_word_across_years(year_from, year_to, word)

@app.get("/xyz/{year}")
def analogies(year: int, x: str, y: str, z: str):
    positive = [y, z]
    negative = [x]
    return model_data.analogies(year, positive, negative)

@app.get("/tsne/{year}")
async def tsne(year: int, words: str):
    image = model_data.tsne(year, words)
    return Response(content=image, media_type="image/png")