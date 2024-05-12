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
titles = ['음식', '동물', '직업', '스포츠', '과일', '야채', '영화', '만화 캐릭터', '가구', '의류', '음악 악기', '색깔', '꽃', '곤충', '비디오 게임 이름', '역사적 인물', '슈퍼히어로', '디저트', '건축물', '보드 게임', '차량', '교통 수단', '해양 생물', '조류', '공룡', '디지털 기기', '액세서리', '나무', '애니메이션']


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
            **상황**: 당신은 퀴즈 게임의 진행자입니다. 참가자는 특정 주제에 대해 물어보며, 당신은 그 주제에 대한 정보를 제공해야 합니다. 그러나, 특정 단어들은 사용이 금지되어 있습니다.

            **목표**: {titles} 에서 랜덤한 5가지 단어를 제공하되, 금지된 단어들(응답, 대답, 리스트, 단어)을 제외하고, 참가자의 질문과 관련 없는 내용은 배제해야 합니다. 

            **행동 지침**:
            1. {titles} 에서 랜덤한 5개의 단어를 콤마로 구분해 제시합니다.
            2. 금지된 단어들은 사용하지 않습니다.
            3. 참가자의 질문과 관련 없는 내용은 포함하지 않습니다.
            4. 모든 단어는 실제로 존재하는 것만 사용하며, 중복되지 않아야 합니다.
            5. 특수문자는 콤마를 제외하고 사용하지 않습니다.
            6. 반드시 '애니메이션' 또는 '게임' 에 관한 주제를 포함해야합니다.

            **행동**:
            - 참가자의 주제에 대해 깊이 생각하고, 제외해야 할 단어들과 조건들을 염두에 두면서, 관련 있는 5개의 단어를 선정합니다.
            - 선정한 단어들이 조건에 부합하는지 검토합니다.
            - 금지된 단어나 조건에 어긋나는 단어가 있다면, 적절한 단어로 교체합니다.
            - 최종적으로 조건에 맞는 5개의 단어를 콤마로 구분해 참가자에게 제공합니다.

            **결과 확인**:
            - 제공된 단어들이 주제와 관련이 있고, 금지된 단어를 포함하지 않는지 확인합니다.
            - 모든 조건이 충족되었다면, 참가자에게 답변을 제공합니다.
            - 만약 조건을 충족하지 못했다면, 수정이 필요한 부분을 파악하고 조건에 맞는 답변을 다시 준비합니다. 
        """,
        input_variables=["titles", "number"]
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
            **상황**: 당신은 퀴즈 게임의 진행자입니다. 참가자는 특정 주제에 대해 물어보며, 당신은 그 주제에 대한 정보를 제공해야 합니다. 그러나, 특정 단어들은 사용이 금지되어 있습니다.

            **목표**: {title}에 대해 5개의 관련 단어를 제공하되, {before_subjects}와 금지된 단어들(응답, 대답, 리스트, {title}, 단어)을 제외하고, 참가자의 질문과 관련 없는 내용은 배제해야 합니다. 

            **행동 지침**:
            1. 참가자가 제시한 주제인 {title}에 관한 5개의 단어를 콤마로 구분해 제시합니다.
            2. 금지된 단어들은 사용하지 않습니다.
            3. 참가자의 질문과 관련 없는 내용은 포함하지 않습니다.
            4. 모든 단어는 실제로 존재하는 것만 사용하며, 중복되지 않아야 합니다.
            5. 특수문자는 콤마를 제외하고 사용하지 않습니다.
            6. 로마 숫자는 아라비아 숫자로 변환합니다.

            **행동**:
            - 참가자의 주제에 대해 깊이 생각하고, 제외해야 할 단어들과 조건들을 염두에 두면서, 관련 있는 20개의 단어를 선정합니다.
            - 선정한 단어들이 조건에 부합하는지 검토합니다.
            - 금지된 단어나 조건에 어긋나는 단어가 있다면, 적절한 단어로 교체합니다.
            - 최종적으로 조건에 맞는 5개의 단어를 콤마로 구분해 참가자에게 제공합니다.

            **결과 확인**:
            - 제공된 단어들이 주제와 관련이 있고, 금지된 단어를 포함하지 않는지 확인합니다.
            - 모든 조건이 충족되었다면, 참가자에게 답변을 제공합니다.
            - 만약 조건을 충족하지 못했다면, 수정이 필요한 부분을 파악하고 조건에 맞는 답변을 다시 준비합니다. 
        """,
        input_variables=["title", "before_subject"]
    )

    chain = prompt | chat | CommaOutputParser()
    result = chain.invoke({
        "title": filterTitle(data.title),
        "before_subjects": data.before_subjects

    })

    data.subjects = result
    # return secondQuestion(data, example_prompt, examples)
    return data

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