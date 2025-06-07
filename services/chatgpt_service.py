from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.prompts.few_shot import FewShotPromptTemplate
from langchain.schema import BaseOutputParser
from typing import List, Optional
from dotenv import load_dotenv
import os

load_dotenv()
chat = ChatOpenAI(
    temperature=0.1,
    model="gpt-4o",
    api_key=os.getenv("OPENAI_API_KEY"),
)

# 결과를 파싱하기 위한 outputParser
class CommaOutputParser(BaseOutputParser):
    def parse(self, text):
        items = text.strip().split(",")  # comma 기준으로 구분
        return list(map(str.strip, items))  # list 를 return

def get_title(number: int, excluded_titles: List[str] = None):
    """
    catchmind에 적합한 대주제를 동적으로 생성하는 함수
    
    Args:
        number (int): 생성할 대주제 개수
        excluded_titles (List[str], optional): 이전에 사용된 대주제들 (중복 방지)
    
    Returns:
        List[str]: 생성된 대주제들
    """
    if excluded_titles is None:
        excluded_titles = []
    
    example_prompt = PromptTemplate.from_template(
        """
        Human: {question}
        AI: {answer}
        """
    )

    examples = [
        {
            "question": "캐치마인드 게임용 대주제 5개를 생성해주세요.",
            "answer": "동물, 음식, 교통수단, 악기, 과일"
        },
        {
            "question": "이전과 다른 새로운 캐치마인드 대주제들을 만들어주세요.",
            "answer": "가구, 운동용품, 건물, 채소, 장난감"
        },
        {
            "question": "그림으로 그리기 적합한 카테고리들을 추천해주세요.",
            "answer": "꽃, 곤충, 의류, 주방용품, 문구용품"
        }
    ]

    prompt = FewShotPromptTemplate(
        example_prompt=example_prompt,
        examples=examples,
        suffix="""
        **상황**: 당신은 캐치마인드 게임의 전문 기획자입니다. 플레이어들이 그림으로 표현하고 맞출 수 있는 최적의 대주제들을 생성해야 합니다.

        **목표**: 캐치마인드 게임에 적합한 {number}개의 대주제를 동적으로 생성하되, 기존에 사용된 주제들({excluded_titles})과 중복되지 않도록 해야 합니다.

        **캐치마인드 대주제 생성 기준**:
        1. **시각적 표현 가능성**: 그림으로 그리기 쉽고 직관적으로 인식 가능한 카테고리
        2. **구체성**: 추상적 개념이 아닌 구체적이고 명확한 명사 카테고리
        3. **포괄성**: 해당 카테고리 안에 10-20개의 세부 항목들을 포함할 수 있는 범위
        4. **보편성**: 문화적 배경에 관계없이 대부분의 사람들이 이해할 수 있는 주제
        5. **적절한 난이도**: 너무 쉽지도 어렵지도 않은 적당한 수준

        **생성 가능한 대주제 카테고리 예시**:
        - 생물계: 동물, 곤충, 바다생물, 새, 꽃, 나무 등
        - 음식: 과일, 채소, 디저트, 음료, 빵류 등  
        - 사물: 가구, 악기, 운동용품, 문구용품, 주방용품 등
        - 장소: 건물, 랜드마크, 자연풍경 등
        - 교통: 교통수단, 이동기구 등
        - 패션: 의류, 액세서리, 신발 등

        **피해야 할 대주제들**:
        - 추상적 개념: 감정, 철학, 이론, 개념 등
        - 직업이나 역할: 사람의 행동으로만 표현 가능한 것들
        - 색깔이나 패턴: 그 자체로는 그림의 주제가 될 수 없는 것들
        - 너무 복잡한 것들: 역사적 사건, 복잡한 기술 등

        **행동 지침**:
        1. 제외 대상 ({excluded_titles})과 절대 중복되지 않는 새로운 주제들만 생성
        2. 각 대주제는 캐치마인드 게임에 최적화된 것인지 검증
        3. 생성한 주제들이 서로 너무 유사하지 않도록 다양성 확보
        4. 모든 주제는 실제 존재하며 그리기 가능한 것들로만 구성
        5. 콤마로 구분하여 정확히 {number}개만 제시

        **출력 형식**: 콤마로 구분된 {number}개의 대주제만 출력 (설명이나 부가 내용 없이)

        **결과 검증**:
        - 각 주제가 그림으로 표현하기 적합한가?
        - 제외 목록과 중복되지 않는가?
        - 하위 소주제들을 충분히 포함할 수 있는가?
        - 게임 플레이어들이 이해하기 쉬운가?
        """,
        input_variables=["number", "excluded_titles"]
    )

    chain = prompt | chat | CommaOutputParser()
    result = chain.invoke({
        "number": number,
        "excluded_titles": excluded_titles
    })
    
    return result


def get_subject(title: str, number: int = 5, before_subjects: List[str] = None, difficulty: str = "medium"):
    """
    대주제에 맞는 소주제들을 동적으로 생성하는 함수
    
    Args:
        title (str): 대주제명 (예: '동물', '음식')
        number (int): 생성할 소주제 개수 (기본 5개)
        before_subjects (List[str], optional): 이전에 사용된 소주제들 (중복 방지)
        difficulty (str): 난이도 ('easy', 'medium', 'hard')
    
    Returns:
        List[str]: 생성된 소주제들
    """
    if before_subjects is None:
        before_subjects = []
    
    example_prompt = PromptTemplate.from_template(
        """
        Human: {question}
        AI: {answer}
        """
    )

    examples = [
        {
            "question": "대주제 '동물'에 대한 캐치마인드 소주제 5개를 생성해주세요.",
            "answer": "호랑이, 코끼리, 펭귄, 기린, 고양이"
        },
        {
            "question": "대주제 '음식'에 적합한 그리기 쉬운 항목들을 추천해주세요.",
            "answer": "피자, 햄버거, 초밥, 파스타, 케이크"
        },
        {
            "question": "대주제 '교통수단'의 캐치마인드 소주제들을 만들어주세요.",
            "answer": "자동차, 기차, 비행기, 자전거, 배"
        },
        {
            "question": "대주제 '가구'에 맞는 그림으로 표현하기 좋은 항목들을 생성해주세요.",
            "answer": "의자, 테이블, 침대, 소파, 책장"
        },
        {
            "question": "대주제 '과일'에 속하는 캐치마인드 소주제들을 만들어주세요.",
            "answer": "사과, 바나나, 오렌지, 포도, 딸기"
        }
    ]

    prompt = FewShotPromptTemplate(
        example_prompt=example_prompt,
        examples=examples,
        suffix="""
        **상황**: 당신은 캐치마인드 게임의 전문 컨텐츠 제작자입니다. 주어진 대주제에 맞는 최적의 소주제들을 생성해야 합니다.

        **목표**: 대주제 '{title}'에 속하는 {number}개의 소주제를 생성하되, 이전에 사용된 항목들({before_subjects})과 중복되지 않고 캐치마인드 게임에 최적화된 항목들을 만들어야 합니다.

        **캐치마인드 소주제 생성 기준**:
        1. **대주제 일치성**: 반드시 '{title}' 카테고리에 명확히 속하는 항목들만 선택
        2. **그리기 적합성**: 펜이나 연필로 그려서 표현할 수 있는 구체적인 형태
        3. **시각적 구별성**: 그림만 보고도 다른 것과 구별할 수 있는 특징적 형태
        4. **적절한 복잡도**: 너무 단순하지도 복잡하지도 않은 {difficulty} 수준
        5. **문화적 보편성**: 다양한 문화권 사람들이 알 수 있는 일반적인 것들

        **난이도별 기준**:
        - easy: 일상생활에서 자주 접하는 기본적인 것들 (예: 고양이, 사과, 자동차)
        - medium: 적당한 인지도를 가진 표준적인 것들 (예: 기린, 아보카도, 헬리콥터)
        - hard: 좀 더 세분화되거나 전문적이지만 여전히 그리기 가능한 것들 (예: 카멜레온, 두리안, 잠수함)

        **생성 제한사항**:
        - **절대 금지**: {before_subjects}에 포함된 항목들과 동일하거나 유사한 것들
        - **추상적 개념 금지**: 감정, 행동, 상태 등 형태가 없는 것들  
        - **너무 세부적인 것 금지**: 구별하기 어려울 정도로 비슷한 것들
        - **부적절한 내용 금지**: 논란이 될 수 있는 내용들
        - **브랜드명 금지**: 특정 브랜드나 상표명이 아닌 일반명사 사용

        **행동 지침**:
        1. 대주제 '{title}'의 정의를 명확히 이해하고 그에 정확히 속하는 항목들만 선택
        2. 각 항목이 캐치마인드 게임에서 그리기 적합한지 검증
        3. {before_subjects}와 절대 중복되지 않는 새로운 항목들만 생성
        4. 생성된 항목들이 서로 너무 유사하지 않도록 다양성 확보
        5. {difficulty} 난이도에 맞는 적절한 수준의 항목들 선택
        6. 모든 항목은 실제 존재하는 것들로만 구성
        7. 특수문자나 숫자 없이 순수한 한글 명사만 사용

        **출력 형식**: 콤마로 구분된 {number}개의 소주제만 출력 (설명이나 부가 내용 없이)

        **최종 검증 체크리스트**:
        ✓ 모든 항목이 '{title}' 대주제에 정확히 속하는가?
        ✓ 그림으로 그리기 적합하고 시각적으로 구별 가능한가?
        ✓ {before_subjects}와 중복되지 않는가?
        ✓ {difficulty} 난이도에 적절한가?
        ✓ 문화적으로 보편적이고 일반적인 것들인가?
        ✓ 서로 다양하고 차별화된 항목들인가?
        """,
        input_variables=["title", "number", "before_subjects", "difficulty"]
    )

    chain = prompt | chat | CommaOutputParser()
    result = chain.invoke({
        "title": title,
        "number": number,
        "before_subjects": before_subjects,
        "difficulty": difficulty
    })
    
    return result