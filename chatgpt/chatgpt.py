from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.prompts.few_shot import FewShotPromptTemplate
from langchain.schema import BaseOutputParser
from Model.GameSubject import GameSubject
from dotenv import load_dotenv
import os

load_dotenv()
chat = ChatOpenAI(
    temperature=0.8,
    model="gpt-3.5-turbo-0125",
    api_key=os.getenv("OPENAI_API_KEY"),
)

## 결과를 파싱하기 위한 outputParser
class CommaOutputParser(BaseOutputParser):
    def parse(self, text):
        items = text.strip().split(",") # comma 기준으로 구분
        return list(map(str.strip, items)) # list 를 return


def suggest(data : GameSubject):
    examples = [
        {
            "question" : "'동물' 주제 5개를 제시해. 대답은 모두 단어여야만 해",
            "answer" : """
                고양이, 강아지, 참새, 호랑이, 코끼리
            """
        },
        {
            "question" : "'하늘' 카테고리에 대해 5개의 주제를 제시해.",
            "answer" : """
                독수리, 비행기, 구름, 풍선, 열기구
            """
        },
        {
            "question" : "'바다' 카테고리에 대해 5개의 주제를 제시해.",
            "answer" : """
                배, 등대, 소라, 돌고래, 상어
            """
        },
    ]

    example_prompt = PromptTemplate.from_template(
         """
            Human : {question}
            AI : {answer}
        """
    )

    prompt = FewShotPromptTemplate(
        example_prompt=example_prompt,
        examples=examples,
        suffix="""
           너는 리스트 생성 머신이야. 내가 질문한 모든 대답에 대해서 콤마로 구분된 리스트로 제시해. 
            다양한 '{subject} 이름' 5개를 제시해. 
            Do NOT reply with anything else.
            단 아래 조건을 반드시 따라야해. 
            1. 중복된 단어는 없어야해
            2. 답변에 {subject} 는 붙이지마
            3. 주제 5개 외 다른 말은 붙이지마
            4. 한글로 대답해
            5. {be_subject} 의 내용과는 절대 중복되면 안돼
        """,
        input_variables=["subject"]
    )


    chain = prompt | chat | CommaOutputParser()
    result = chain.invoke({
        "subject" : data.selected_subject,
        "be_subject" : data.before_suject
    })

    data.suggested_subject = result
    return data