from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.prompts.few_shot import FewShotPromptTemplate
from Model.GameSubject import GameSubject
from dotenv import load_dotenv
import os

load_dotenv()
chat = ChatOpenAI(
    temperature=0.7,
    model="gpt-3.5-turbo-0125",
    api_key=os.getenv("OPENAI_API_KEY"),
)


def suggest(subject : str):
    examples = [
        {
            "question" : "catchmind 게임에서 사용할 수 있는 '동물' 주제 5개를 제시해. 대답은 모두 단어여야만 해",
            "answer" : """
                [고양이, 강아지, 참새, 호랑이, 코끼리]
            """
        },
        {
            "question" : "catchmind 게임에서 사용할 수 있는 '하늘' 주제 5개를 제시해 대답은 모두 단어여야만 해",
            "answer" : """
                [독수리, 비행기, 구름, 풍선, 열기구]
            """
        },
        {
            "question" : "catchmind 게임에서 사용할 수 있는 '바다' 주제 5개를 제시해 대답은 모두 단어여야만 해",
            "answer" : """
                [배, 등대, 소라, 돌고래, 상어]
            """
        }
    ]

    example_prompt = PromptTemplate.from_template(
         """
            "Human" : {question}
            "AI" : {answer}
        """
    )

    prompt = FewShotPromptTemplate(
        example_prompt=example_prompt,
        examples=examples,
        suffix="""
            '{subject}' 카테고리에 대해 5개의 주제를 제시해
            단 아래 조건을 반드시 따라야해. 
            1. 중복된 단어는 없어야해
            3. [] 형식으로 대답해
            2. '인물' 주제에 답변을 제외하고 반드시 하나의 단어로 되어있어야해
        """,
        input_variables=["subject"]
    )


    chain = prompt | chat
    result = chain.invoke({
        "subject" : subject,
    })

    GameSubject.selected_subject = subject
    for data in result.content:
        GameSubject.suggested_subject.append(data)

    return GameSubject