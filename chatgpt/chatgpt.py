from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.prompts.few_shot import FewShotPromptTemplate
from langchain.schema import BaseOutputParser
from Model.GameSubject import GameSubject
from Model.GameTitle import GameTitle
from dotenv import load_dotenv
import os

load_dotenv()
chat = ChatOpenAI(
    temperature=0.1,
    model="gpt-4.1-nano",
    api_key=os.getenv("OPENAI_API_KEY"),
)

class CommaOutputParser(BaseOutputParser):
    def parse(self, text):
        items = text.strip().split(",")
        return [item.strip() for item in items if item.strip()]

titles = ['음식', '동물', '직업', '스포츠', '과일', '야채', '영화', '만화 캐릭터', '가구', '의류', 
          '음악 악기', '색깔', '꽃', '곤충', '비디오 게임 이름', '역사적 인물', '슈퍼히어로', 
          '디저트', '건축물', '보드 게임', '차량', '교통 수단', '해양 생물', '조류', '공룡', 
          '디지털 기기', '액세서리', '나무', '애니메이션']

def get_title(number: int):
    example_prompt = PromptTemplate.from_template(
        "Human: {question}\nAI: {answer}"
    )

    prompt = FewShotPromptTemplate(
        example_prompt=example_prompt,
        examples=[],
        suffix="""
**상황**: Catchmind 게임의 대주제(카테고리) {number}개를 선정해야 합니다.
**목표**: {titles}에서 다음 조건을 만족하는 {number}개의 주제를 골라주세요.

**필수 조건**:
1. 반드시 '애니메이션' 또는 '게임' 중 하나를 포함
2. 실제 존재하며 그림으로 표현 가능한 범주만 선택
3. 중복 없이 랜덤 추출
4. 금지 단어: 응답, 대답, 리스트, 단어

**출력 형식**: 콤마로 구분된 {number}개 단어 (예: 동물, 게임, 음식, 스포츠, 영화)
        """,
        input_variables=["titles", "number"]
    )

    chain = prompt | chat | CommaOutputParser()
    result = chain.invoke({"number": number, "titles": ", ".join(titles)})
    return result[:number]  # 항상 정확한 개수 반환

def get_subject(data: GameSubject, number: int):
    examples = [
        {
            "question": "건축물 주제로 5개의 구체적 단어를 생성해주세요. 이전 단어 [에펠탑, 자유의 여신상]은 제외합니다.",
            "answer": "콜로세움, 타지마할, 버킹엄 궁전, 피사의 사탑, 그레이트월"
        },
        {
            "question": "동물 주제로 3개의 구체적 단어를 생성해주세요. 이전 단어 [호랑이, 사자]는 제외합니다.",
            "answer": "기린, 캥거루, 판다"
        }
    ]

    example_prompt = PromptTemplate.from_template(
        "Human: {question}\nAI: {answer}"
    )

    prompt = FewShotPromptTemplate(
        example_prompt=example_prompt,
        examples=examples,
        suffix="""
**상황**: Catchmind 게임의 소주제(그림 주제) {number}개를 생성해야 합니다.
**목표**: '{title}'에 맞는 실제 존재하며 그림 가능한 단어 {number}개를 생성하세요.

**필수 조건**:
1. 이전에 사용된 단어 [{before_subjects}]는 절대 포함 금지
2. 구체적 명사만 선택 (추상적 단어 X)
3. 중복 없이 랜덤 추출
4. 금지 단어: 응답, 대답, 리스트, 단어, 주제

**출력 형식**: 콤마로 구분된 {number}개 단어 (예: 호랑이, 코끼리, 펭귄)
        """,
        input_variables=["title", "before_subjects", "number"]
    )

    chain = prompt | chat | CommaOutputParser()
    result = chain.invoke({
        "title": filterTitle(data.title),
        "before_subjects": ", ".join(data.before_subjects),
        "number": number
    })
    
    data.subjects = [item for item in result if item not in data.before_subjects][:number]
    return data

def filterTitle(title: str):
    return {
        "애니메이션": "일본 애니메이션 캐릭터",
        "게임": "인기 비디오 게임 이름"
    }.get(title, f"{title} 관련 구체적 단어")
