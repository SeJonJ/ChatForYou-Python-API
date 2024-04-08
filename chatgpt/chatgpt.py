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
    temperature=0.8,
    model="gpt-3.5-turbo-0125",
    api_key=os.getenv("OPENAI_API_KEY"),
)

# 결과를 파싱하기 위한 outputParser
class CommaOutputParser(BaseOutputParser):
    def parse(self, text):
        items = text.strip().split(",")  # comma 기준으로 구분
        return list(map(str.strip, items))  # list 를 return

# 캐치마인드 예시 주제
titles = ['음식', '동물', '직업', '스포츠', '과일', '야채', '영화', '만화 캐릭터', '가구', '의류', '음악 악기', '색깔', '꽃', '곤충', '비디오 게임', '역사적 인물', '슈퍼히어로', '디저트', '건축물', '보드 게임', '차량', '교통 수단', '해양 생물', '조류', '공룡', '디지털 기기', '액세서리', '나무', '애니메이션']


def get_title(number : int):

    example_prompt = PromptTemplate.from_template(
        """
            Human : {question}
            AI : {answer}
        """
    )

    prompt = FewShotPromptTemplate(
        example_prompt=example_prompt,
        examples=[],
        suffix="""
            {titles} 에서 {number}개를 랜덤하게 조합해서 선택한 후 콤마로 구분된 리스트로 답변만 제시해.
            단 애니메이션과 게임 둘 중 하나는 반드시 포함해
            응답 외에 다른 대답은 필요없어
        """,
        input_variables=["number"]
    )

    chain = prompt | chat | CommaOutputParser()
    result = chain.invoke({
        "number" : number,
        "titles" : titles
    })
    
    return result


def get_subject(data: GameSubject):
    examples = [
        {
            "question": "'동물' 주제 5개를 제시해. 대답은 모두 단어여야만 해",
            "answer": """
                고양이, 강아지, 참새, 호랑이, 코끼리
            """
        },
        {
            "question": "'하늘' 카테고리에 대해 5개의 주제를 제시해.",
            "answer": """
                독수리, 비행기, 구름, 풍선, 열기구
            """
        },
        {
            "question": "'나라 이름' 카테고리에 대해 5개의 주제를 제시해.",
            "answer": """
                한국, 미국, 일본, 프랑스, 독일
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
            너는 리스트 생성 머신이야. 내가 질문한 모든 대답에 대해서 반드시 콤마로 구분된 리스트로 제시해. 
            가능한 다양한 '{title}' 5개를 한글로 대답해.
            내가 질문한 내용을 제외한 다른 내용은 절대 포함하지마. 
            단 반드시 조건을 지켜야하며 조건을 지키지못하면 조건을 지킬 수 있을때까지 대답하지마.
            0. 다음 단어는 응답에서 반드시 제외해 : 응답, 대답, 리스트, {title}, 단어
            1. 내가 물어본 질문과 관련없는 내용들은 반드시 모두 제외해. 또한 내가 질문한 내용을 다시 작성하지마.
            2. 중복된 단어는 없어야해
            3. {before_subjects} 와 절대 중복되면 안돼.
            4. {title} 이 '애니메이션' 과 관련된 주제라면 [원피스, 나루토, 블리치] 중 2가지는 제외하고 대답해.
            5. {title} 이 '게임' 과 관련된 주제라면 [리그오브레전드, 워크프래프트, 리니지, 메이플스토리] 중 2가지는 제외하고 대답해
        """,
        input_variables=["title"]
    )

    chain = prompt | chat | CommaOutputParser()
    result = chain.invoke({
        "title": filterTitle(data.title),
        "before_subjects": data.before_subjects
    })

    data.subjects = result
    return data


def filterTitle(title: str):
    if title == "애니메이션":
        return "2000년대 유명한 애니메이션 제목"
    elif title == "게임":
        return "다양한 장르의 온라인 게임 제목"
    else:
        return title + " 이름"
