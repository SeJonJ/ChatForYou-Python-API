from typing import Union
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from Model.GameSubject import GameSubject
from chatgpt import chatgpt
from dotenv import load_dotenv
import os

load_dotenv()
app = FastAPI()
app.add_middleware( ## CORS 에러 해결을 위한 설정
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

@app.post("/game_subject")
def game_subject(data : GameSubject):
    print("model :: ", data)
    data = chatgpt.suggest(data)
    return {"result" : data}


if __name__ == "__main__":
    ## uvicorn 이용할 때 명령어를 사용할 수도 있으나 아래처럼 설정 하면 python3 main.py 처럼 단순 실행도 가능
    uvicorn.run("main:app",host='0.0.0.0', port=8000, reload=True,)