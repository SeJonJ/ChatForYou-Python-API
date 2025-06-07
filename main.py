from typing import Union
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from model.GameSubject import GameSubject
from model.GameTitle import GameTitle
from gpt_api import chatgpt
from dotenv import load_dotenv
import os

load_dotenv()
app = FastAPI()
app.add_middleware( ## CORS 에러 해결을 위한 설정
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "https://localhost:8443","https://hjproject.kro.kr", "https://hjproject.kro.kr/chatforyou"],
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

@app.get("/game_titles")
def game_subject(data : GameTitle | None = None, response_model=GameTitle):
    if data is None:
        data = GameTitle()
    result = chatgpt.get_title(data.number, data.excluded_titles)
    return {"titles" : result}

@app.post("/game_subjects")
def game_subject(data : GameSubject, response_model=GameSubject):
    result = chatgpt.get_subject(data.title, data.number, data.before_subjects, data.difficulty)
    return {
        "title" : data.title,
        "subjects" : result,
        "before_subjects" : data.before_subjects,
        "difficulty" : data.difficulty
    }

if __name__ == "__main__":
    ## uvicorn 이용할 때 명령어를 사용할 수도 있으나 아래처럼 설정 하면 python3 main.py 처럼 단순 실행도 가능
    uvicorn.run("main:app",host='0.0.0.0', port=8000, reload=True,)