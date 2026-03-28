from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.prompts.few_shot import FewShotPromptTemplate
from langchain.schema import BaseOutputParser
from typing import List, Optional
from dotenv import load_dotenv
import os

load_dotenv()

# 대주제 생성용: 다양한 카테고리 필요 → 높은 temperature
title_chat = ChatOpenAI(
    temperature=0.7,
    model="gpt-4o-mini",
    api_key=os.getenv("OPENAI_API_KEY"),
)

# 소주제 생성용: 적절히 다양하되 대주제 범위 내 → 중간 temperature
subject_chat = ChatOpenAI(
    temperature=0.5,
    model="gpt-4o-mini",
    api_key=os.getenv("OPENAI_API_KEY"),
)

# 결과를 파싱하기 위한 outputParser (유효성 검증 포함)
class CommaOutputParser(BaseOutputParser):
    def parse(self, text):
        items = text.strip().split(",")
        items = [item.strip() for item in items if item.strip()]  # 빈 문자열 제거
        items = [item for item in items if len(item) >= 2]        # 최소 2글자 필터
        items = list(dict.fromkeys(items))                         # 중복 제거 (순서 유지)
        return items

# TODO: 난이도(difficulty)는 현재 "medium" 고정. 추후 라운드 진행에 따라 동적으로 조절 가능하도록 개선 예정
def get_title(number: int, excluded_titles: List[str] = None, difficulty: str = "medium"):
    """
    catchmind에 적합한 대주제를 동적으로 생성하는 함수
    
    Args:
        number (int): 생성할 대주제 개수
        excluded_titles (List[str], optional): 이전에 사용된 대주제들 (중복 방지)
        difficulty (str): 난이도 ('easy', 'medium', 'hard')
    
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
            "question": "캐치마인드 게임용 easy 난이도 대주제 5개를 생성해주세요.",
            "answer": "동물, 음식, 교통수단, 과일, 애니메이션 캐릭터"
        },
        {
            "question": "캐치마인드 게임용 medium 난이도 대주제 5개를 생성해주세요.",
            "answer": "해양생물, 디저트, 악기, 게임 캐릭터, 운동용품"
        },
        {
            "question": "캐치마인드 게임용 hard 난이도 대주제 5개를 생성해주세요.",
            "answer": "파충류, 현악기, 영화 속 캐릭터, 캠핑용품, 수공예도구"
        }
    ]

    prompt = FewShotPromptTemplate(
        example_prompt=example_prompt,
        examples=examples,
        suffix="""
        **상황**: 당신은 10년간 보드게임/파티게임을 기획해온 전문가입니다.
        당신의 핵심 원칙은:
        1. 모든 연령대(8세~60세)가 즐길 수 있는 보편적 주제 선택
        2. "그리는 사람"과 "맞추는 사람" 모두에게 적절한 난이도 유지
        3. 반복 플레이해도 지루하지 않은 다양성 확보

        **목표**: 캐치마인드 게임에 적합한 {number}개의 대주제를 {difficulty} 난이도로 생성하되, 기존에 사용된 주제들({excluded_titles})과 중복되지 않도록 해야 합니다.

        **난이도별 대주제 기준**:
        - easy: 일상적이고 친숙한 카테고리 (예: 동물, 과일, 교통수단)
        - medium: 약간 전문적이지만 대부분 알 수 있는 카테고리 (예: 해양생물, 디저트, 악기)
        - hard: 세분화되거나 특수한 카테고리 (예: 파충류, 열대과일, 현악기)

        **캐치마인드 대주제 생성 기준**:
        1. **시각적 표현 가능성**: 그림으로 그리기 쉽고 직관적으로 인식 가능한 카테고리
        2. **구체성**: 추상적 개념이 아닌 구체적이고 명확한 명사 카테고리
        3. **포괄성**: 해당 카테고리 안에 10-20개의 세부 항목들을 포함할 수 있는 범위
        4. **보편성**: 문화적 배경에 관계없이 대부분의 사람들이 이해할 수 있는 주제
        5. **적절한 난이도**: {difficulty} 수준에 맞는 주제 선택

        **생성 가능한 대주제 카테고리 예시**:
        - 생물계: 동물, 곤충, 바다생물, 새, 꽃, 나무 등
        - 음식: 과일, 채소, 디저트, 음료, 빵류 등  
        - 사물: 가구, 악기, 운동용품, 문구용품, 주방용품 등
        - 장소: 건물, 랜드마크, 자연풍경 등
        - 교통: 교통수단, 이동기구 등
        - 패션: 의류, 액세서리, 신발 등

        **필수 포함 규칙**:
        - 생성하는 대주제 중 **최소 1개**는 반드시 [비디오 게임], [일본 애니메이션], [온라인 게임] 중에서 선택해야 합니다.

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
        - 각 주제가 {difficulty} 난이도에 적합한가?
        - 각 주제가 그림으로 표현하기 적합한가?
        - 제외 목록과 중복되지 않는가?
        - 하위 소주제들을 충분히 포함할 수 있는가?
        - 게임 플레이어들이 이해하기 쉬운가?
        """,
        input_variables=["number", "excluded_titles", "difficulty"]
    )

    chain = prompt | title_chat | CommaOutputParser()
    result = chain.invoke({
        "number": number,
        "excluded_titles": excluded_titles,
        "difficulty": difficulty
    })
    
    return result


# TODO: 난이도(difficulty)는 현재 "medium" 고정. 추후 라운드 진행에 따라 동적으로 조절 가능하도록 개선 예정
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
            "question": "대주제 '동물'에 대한 easy 난이도 캐치마인드 소주제 5개를 생성해주세요.",
            "answer": "고양이, 강아지, 토끼, 물고기, 돼지"
        },
        {
            "question": "대주제 '동물'에 대한 medium 난이도 캐치마인드 소주제 5개를 생성해주세요.",
            "answer": "기린, 펭귄, 코알라, 하마, 독수리"
        },
        {
            "question": "대주제 '동물'에 대한 hard 난이도 캐치마인드 소주제 5개를 생성해주세요.",
            "answer": "카멜레온, 아르마딜로, 해마, 오리너구리, 순록"
        },
        {
            "question": "대주제 '음식'에 대한 easy 난이도 캐치마인드 소주제 5개를 생성해주세요.",
            "answer": "피자, 햄버거, 김밥, 라면, 케이크"
        },
        {
            "question": "대주제 '음식'에 대한 hard 난이도 캐치마인드 소주제 5개를 생성해주세요.",
            "answer": "크루아상, 꼬치구이, 뇨끼, 나시고렝, 에클레어"
        },
        {
            "question": "대주제 '가구'에 맞는 medium 난이도 캐치마인드 소주제 5개를 생성해주세요.",
            "answer": "흔들의자, 이층침대, 진열장, 화장대, 신발장"
        },
        {
            "question": "대주제 '비디오 게임'에 대한 medium 난이도 캐치마인드 소주제 5개를 생성해주세요.",
            "answer": "젤다의전설, 슈퍼마리오, 포켓몬스터, 디아블로, 언차티드"
        },
        {
            "question": "대주제 '일본 애니메이션'에 대한 medium 난이도 캐치마인드 소주제 5개를 생성해주세요.",
            "answer": "원피스, 나루토, 드래곤볼, 슬램덩크, 진격의거인"
        },
        {
            "question": "대주제 '온라인 게임'에 대한 medium 난이도 캐치마인드 소주제 5개를 생성해주세요.",
            "answer": "리그 오브 레전드, 마인크래프트, 오버워치, 발로란트, 메이플스토리"
        }
    ]

    prompt = FewShotPromptTemplate(
        example_prompt=example_prompt,
        examples=examples,
        suffix="""
        **상황**: 당신은 10년간 보드게임/파티게임을 기획해온 전문가입니다.
        당신의 핵심 원칙은:
        1. 모든 연령대(8세~60세)가 즐길 수 있는 보편적 주제 선택
        2. "그리는 사람"과 "맞추는 사람" 모두에게 적절한 난이도 유지
        3. 반복 플레이해도 지루하지 않은 다양성 확보

        **목표**: 대주제 '{title}'에 속하는 {number}개의 소주제를 생성하되, 이전에 사용된 항목들({before_subjects})과 중복되지 않고 캐치마인드 게임에 최적화된 항목들을 만들어야 합니다.

        **캐치마인드 소주제 생성 기준**:
        1. **대주제 일치성**: 반드시 '{title}' 카테고리에 명확히 속하는 항목들만 선택
        2. **그리기 적합성**: 펜이나 연필로 그려서 표현할 수 있는 구체적인 형태
        3. **시각적 구별성**: 그림만 보고도 다른 것과 구별할 수 있는 특징적 형태
        4. **적절한 복잡도**: 너무 단순하지도 복잡하지도 않은 {difficulty} 수준
        5. **문화적 보편성**: 다양한 문화권 사람들이 알 수 있는 일반적인 것들
        6. **중복 금지**: {before_subjects}에 포함된 항목들과 동일한 것들
        7. **이름 주제 금지**: 이름 주제는 금지
        8. **글자수 제한**: 소주제는 최소 두 글자 이상

        **난이도별 기준**:
        - easy: 일상생활에서 자주 접하는 기본적인 것들 (예: 고양이, 사과, 자동차)
        - medium: 적당한 인지도를 가진 표준적인 것들 (예: 기린, 아보카도, 헬리콥터)
        - hard: 좀 더 세분화되거나 전문적이지만 여전히 그리기 가능한 것들 (예: 카멜레온, 두리안, 잠수함)

        **생성 제한사항**:
        - **절대 금지**: {before_subjects}에 포함된 항목들과 동일하거나 유사한 것들
        - **동의어/유사어 금지**: 같은 대상을 다르게 부르는 것들은 모두 중복으로 간주
          예시: "자전거"="바이크", "핸드폰"="스마트폰", "아이스크림"="빙과"
        - **상위/하위 개념 중복 금지**: 이미 나온 항목의 상위/하위 개념도 제외
          예시: "강아지"가 있으면 "푸들", "골든리트리버" 등도 제외
        - **추상적 개념 금지**: 감정, 행동, 상태 등 형태가 없는 것들  
        - **너무 세부적인 것 금지**: 구별하기 어려울 정도로 비슷한 것들
        - **부적절한 내용 금지**: 논란이 될 수 있는 내용들
        - **브랜드명 금지**: 특정 브랜드나 상표명이 아닌 일반명사 사용
          ⚠️ **단, 대주제가 '비디오 게임', '일본 애니메이션', '온라인 게임'인 경우는 예외**: 이 경우 소주제는 반드시 **실제 작품명/게임명**이어야 합니다.

        **엔터테인먼트 대주제 특별 규칙** (대주제가 '비디오 게임', '일본 애니메이션', '온라인 게임'인 경우):
        - 소주제는 반드시 **실제 존재하는 게임명 또는 애니메이션명**이어야 합니다
        - '조작', '전투', '레벨업', '퀘스트' 같은 게임 내 용어/개념은 **절대 금지**합니다
        - 줄임말은 허용하지 않습니다 (예: 젤다의전설(o)->젤다(x), 슈퍼마리오(o)->마리오(x), 리그 오브 레전드(o)->롤(x), 던전앤파이터(o)->던파(x))
        - 시리즈 번호는 붙이지 않고 시리즈명만 사용합니다 (예: 디아블로(o)->디아블로3(x), 콜 오브 듀티(o)->콜 오브 듀티4(x), 파이널 판타지(o)->파이널 판타지7(x))
        - 비디오 게임 소주제 예시: 언차티드, 헤일로, 젤다의전설, 슈퍼마리오, 포켓몬스터, 디아블로
        - 일본 애니메이션 소주제 예시: 강철의연금술사, 원피스, 나루토, 드래곤볼, 슬램덩크, 진격의거인, 귀멸의칼날, 주술회전, 스파이패밀리, 체인소맨, 나의히어로아카데미아, 디지몬, 유희왕
        - 온라인 게임 소주제 예시: 리그 오브 레전드, 마인크래프트, 로스트아크, 오버워치, 발로란트, 던전앤파이터, 메이플스토리

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
        ✓ 동의어, 유사어, 상위/하위 개념이 겹치지 않는가?
        ✓ {difficulty} 난이도에 적절한가?
        ✓ 문화적으로 보편적이고 일반적인 것들인가?
        ✓ 서로 다양하고 차별화된 항목들인가?
        """,
        input_variables=["title", "number", "before_subjects", "difficulty"]
    )

    chain = prompt | subject_chat | CommaOutputParser()
    result = chain.invoke({
        "title": title,
        "number": number,
        "before_subjects": before_subjects,
        "difficulty": difficulty
    })
    
    return result