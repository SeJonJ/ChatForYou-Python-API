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
    model="gpt-4-turbo",
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
            "question": """ 
                너는 나의 퀴즈 게임 진행을 위해서 만들어진 리스트 생성 머신이야. 
                너가 대답해야 하는 주제는 '건축물' 이고, 주제에 맞는 20 개의 단어를 콤마로 구분된 리스트로 제시해. 
                리스트에는 번호를 붙일 필요가 없고, 내가 질문한 내용을 제외한 다른 내용은 절대 포함하지마. 
            """,
            "answer": """
                호랑이, 사자, 코끼리, 기린, 캥거루, 판다, 고릴라, 늑대, 펭귄, 악어, 뱀, 돌고래, 고래, 오리, 독수리, 토끼, 여우, 하마, 코알라, 사슴.
            """
        },
        {
            "question": """
                너는 나의 퀴즈 게임 진행을 위해서 만들어진 리스트 생성 머신이야. 
                너가 대답해야 하는 주제는 '건축물' 이고, 주제에 맞는 20 개의 단어를 콤마로 구분된 리스트로 제시해. 
                리스트에는 번호를 붙일 필요가 없고, 내가 질문한 내용을 제외한 다른 내용은 절대 포함하지마. 
            """,
            "answer": """
                에펠탑, 자유의 여신상, 콜로세움, 타지마할, 버킹엄 궁전, 피사의 사탑, 그레이트월, 루브르 박물관, 센트럴 파크, 시드니 오페라 하우스, 두바이의 버즈 칼리파, 빅벤, 황금문교, 개선문, 알함브라 궁전, 가우디의 사그라다 파밀리아, 모아이 석상, 시온성당, 소피아 대성당, 포르투갈의 벨렘탑.
            """
        },
        {
            "question": """
            너는 나의 퀴즈 게임 진행을 위해서 만들어진 리스트 생성 머신이야. 
            너가 대답해야 하는 주제는 '나라 이름' 이고, 주제에 맞는 20 개의 단어를 콤마로 구분된 리스트로 제시해. 
            리스트에는 번호를 붙일 필요가 없고, 내가 질문한 내용을 제외한 다른 내용은 절대 포함하지마. 
            """,
            "answer": """
                캐나다, 브라질, 호주, 이탈리아, 일본, 멕시코, 인도, 러시아, 프랑스, 독일, 아르헨티나, 남아프리카 공화국, 이집트, 네덜란드, 벨기에, 스웨덴, 스페인, 그리스, 중국, 터키
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
            너는 나의 퀴즈 게임 진행을 위해서 만들어진 리스트 생성 머신이야. 
            너가 대답해야 하는 주제는 {title} 이고, {before_subjects} 를 제외한 20 개의 단어를 콤마로 구분된 리스트로 제시해. 
            리스트에는 번호를 붙일 필요가 없고, 내가 질문한 내용을 제외한 다른 내용은 절대 포함하지마. 
            단 반드시 조건을 지켜야하며 조건을 지키지못하면 조건을 지킬 수 있을때까지 대답하지마.
            0. 다음 단어는 응답에서 반드시 제외해 : 응답, 대답, 리스트, {title}, 단어
            1. 내가 물어본 질문과 관련없는 내용들은 반드시 모두 제외해. 또한 내가 질문한 내용을 다시 작성하지마.
            3. 답변의 콤마를 제외한 모든 특수문자를 제거하고 중복되는 단어가 없도록 해
            4. 반드시 실제로 존재하는 답변을 제시해
        """,
        input_variables=["title"]
    )

    chain = prompt | chat | CommaOutputParser()
    result = chain.invoke({
        "title": filterTitle(data.title),
        "before_subjects": data.before_subjects

    })

    data.subjects = result
    return secondQuestion(data, example_prompt, examples)


def filterTitle(title: str):
    if title == "애니메이션":
        return "다양한 일본 만화"
    elif title == "게임":
        return "다양한 장르의 온라인 게임 이름"
    else:
        return title + " 이름"
    

def secondQuestion(data: GameSubject, example_prompt : list, examples : list):
    prompt = FewShotPromptTemplate(
        example_prompt=example_prompt,
        examples=examples,
        suffix="""
                너는 나의 퀴즈 게임 진행을 위해서 만들어진 리스트 생성 머신이야. 
                총 제시하는 20개의 {subjects} 중에서 5개를 랜덤으로 선정해서 반드시 콤마로 구분된 리스트로 답변해.
                반드시 실제 존재하는 단어만 선택해
                충족하는 답변을 찾을 수 없다면 충족될때까지 연산해서 답변해
            """,
        input_variables=["subjects", "before_subjects"]
    )
    
    chain = prompt | chat | CommaOutputParser()
    result = chain.invoke({
        "title": filterTitle(data.title),
        "subjects": data.subjects,
        "before_subjects": data.before_subjects
    })
    data.subjects = result
    return data