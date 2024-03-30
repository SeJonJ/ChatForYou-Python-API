from typing import Union
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from Model.GameSubject import GameSubject
from chatgpt import chatgpt
from dotenv import load_dotenv
import os

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ORIGINS"),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def index():
    return "Hello World"

@app.get("/test/{test}")
def test( test : str):
    print("path val :: ", test)
    return {"test" : test}

@app.post("/game_subject", response_model=GameSubject)
def game_subject(data : GameSubject):
    print("model :: ", data)
    return chatgpt.suggest(data.selected_subject)


if __name__ == "__main__":
    uvicorn.run("main:app",host='0.0.0.0', port=8000, reload=True,)