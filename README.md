# ChatForYou Python API Server

## 📋 프로젝트 개요

**ChatForYou**는 게임 개발자와 게임 기획자를 위한 AI 기반 게임 콘텐츠 추천 API 서버입니다.

### 🎯 주요 목적
- 게임 개발 과정에서 창의적인 아이디어 발굴 지원
- AI를 활용한 게임 타이틀 및 주제 자동 생성
- 게임 기획 단계에서의 효율성 향상

### ✨ 핵심 기능
1. **게임 타이틀 추천**: 다양한 장르와 스타일의 게임 제목 자동 생성
2. **게임 주제 추천**: 특정 게임 타이틀에 맞는 세부 주제 및 콘텐츠 아이디어 제공
3. **맞춤형 추천**: 이전 추천 내역을 고려한 중복 방지 기능
4. **난이도 조절**: 게임 주제의 복잡도 및 난이도 설정 가능

### 🛠 기술 스택
- **Backend Framework**: FastAPI (Python)
- **AI Engine**: OpenAI ChatGPT API
- **API Architecture**: RESTful API
- **Containerization**: Docker
- **Environment Management**: Python Virtual Environment

### 🌐 서비스 대상
- 게임 개발자 및 기획자
- 인디 게임 개발팀
- 게임 아이디어가 필요한 크리에이터
- 게임 관련 교육 기관

### 🔧 주요 특징
- **CORS 지원**: 웹 애플리케이션에서 직접 호출 가능
- **RESTful API**: 표준화된 HTTP 메서드 사용
- **확장 가능한 구조**: 모듈화된 설계로 기능 확장 용이
- **Docker 지원**: 컨테이너 기반 배포 및 실행

## 📚 목차

- [설치 및 환경 설정](#-설치-및-환경-설정)
- [API 엔드포인트 문서](#-api-엔드포인트-문서)
- [실행 방법 및 사용 예시](#-실행-방법-및-사용-예시)
- [Docker 사용법 및 배포](#-docker-사용법-및-배포)
- [기여하기](#-기여하기)
- [라이선스](#-라이선스)

## 🚀 설치 및 환경 설정

### 📋 시스템 요구사항
- **Python**: 3.11.6 이상
- **운영체제**: Windows, macOS, Linux
- **메모리**: 최소 2GB RAM 권장
- **디스크 공간**: 최소 1GB 여유 공간

### 🔧 설치 과정

#### 1. 저장소 클론
```bash
git clone https://github.com/your-username/ChatForYou_python_api.git
cd ChatForYou_python_api
```

#### 2. Python 가상환경 설정
```bash
# 가상환경 생성
python -m venv .venv

# 가상환경 활성화
# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate
```

#### 3. 의존성 패키지 설치
```bash
# pip 업그레이드
pip install --upgrade pip

# 필요한 패키지 설치
pip install -r requirements.txt
```

### 🔑 환경 변수 설정

#### 1. .env 파일 생성
프로젝트 루트 디렉토리에 `.env` 파일을 생성하고 다음 내용을 추가하세요:

```env
# OpenAI API 설정
OPENAI_API_KEY=your_openai_api_key_here

# 서버 설정 (선택사항)
HOST=0.0.0.0
PORT=8000
DEBUG=True
```

#### 2. OpenAI API 키 발급
1. [OpenAI 웹사이트](https://platform.openai.com/)에 접속
2. 계정 생성 또는 로그인
3. API Keys 섹션에서 새 API 키 생성
4. 생성된 키를 `.env` 파일의 `OPENAI_API_KEY`에 입력

### 📦 주요 의존성 패키지

| 패키지 | 버전 | 용도 |
|--------|------|------|
| fastapi | 0.99.1 | 웹 프레임워크 |
| uvicorn | - | ASGI 서버 |
| langchain | 0.0.332 | LLM 체인 관리 |
| openai | 0.28.0 | OpenAI API 클라이언트 |
| python-dotenv | 1.0.0 | 환경 변수 관리 |
| pydantic | 1.10.12 | 데이터 검증 |

### ⚠️ 주의사항

1. **API 키 보안**: `.env` 파일은 Git 커밋 X
2. **가상환경**: 반드시 가상환경을 사용하여 의존성 충돌을 방지하세요
3. **Python 버전**: Python 3.11.6 이상 사용을 권장합니다
4. **네트워크**: OpenAI API 호출을 위해 인터넷 연결이 필요합니다

### 🔍 설치 확인

설치가 완료되면 다음 명령어로 정상 작동을 확인할 수 있습니다:

```bash
# 서버 실행 테스트
python main.py

# 또는 uvicorn 직접 실행
uvicorn main:app --reload
```

서버가 정상적으로 시작되면 `http://localhost:8000`에서 "Hello World" 메시지를 확인할 수 있습니다.

## 📚 API 엔드포인트 문서

### 🌐 기본 정보
- **Base URL**: `http://localhost:8000`
- **Content-Type**: `application/json`
- **CORS**: 허용된 도메인에서 직접 호출 가능

### 📋 엔드포인트 목록

#### 1. 🏠 서버 상태 확인
```http
GET /
```

**설명**: 서버가 정상적으로 실행 중인지 확인하는 헬스체크 엔드포인트

**응답**:
```json
"Hello World"
```

**사용 예시**:
```bash
curl -X GET "http://localhost:8000/"
```

---

#### 2. 🧪 테스트 엔드포인트
```http
GET /test/{test}
```

**설명**: 경로 매개변수 테스트용 엔드포인트

**경로 매개변수**:
- `test` (string): 테스트할 문자열

**응답**:
```json
{
  "test": "입력한_테스트_값"
}
```

**사용 예시**:
```bash
curl -X GET "http://localhost:8000/test/hello"
```

---

#### 3. 🎮 게임 타이틀 추천
```http
GET /game_titles
```

**설명**: AI를 활용하여 캐치마인드 게임에 적합한 대주제(타이틀)들을 추천

**쿼리 매개변수** (선택사항):
- `number` (integer): 생성할 타이틀 개수 (기본값: 5)
- `excluded_titles` (array): 제외할 타이틀 목록

**요청 예시**:
```bash
# 기본 요청 (5개 타이틀)
curl -X GET "http://localhost:8000/game_titles"

# 개수 지정
curl -X GET "http://localhost:8000/game_titles?number=3"

# 제외 타이틀 지정
curl -X GET "http://localhost:8000/game_titles?excluded_titles=동물&excluded_titles=음식"
```

**응답 형식**:
```json
{
  "titles": [
    "동물",
    "음식", 
    "교통수단",
    "악기",
    "과일"
  ]
}
```

**응답 필드**:
- `titles` (array): 추천된 게임 타이틀 목록

---

#### 4. 🎯 게임 주제 추천
```http
POST /game_subjects
```

**설명**: 특정 대주제에 맞는 세부 주제들을 AI로 생성

**요청 바디**:
```json
{
  "title": "동물",
  "number": 5,
  "before_subjects": ["고양이", "강아지"],
  "difficulty": "medium"
}
```

**요청 필드**:
- `title` (string, 필수): 대주제명
- `number` (integer, 선택): 생성할 주제 개수 (기본값: 5)
- `before_subjects` (array, 선택): 이전에 사용된 주제들 (중복 방지)
- `difficulty` (string, 선택): 난이도 ("easy", "medium", "hard", 기본값: "medium")

**응답 형식**:
```json
{
  "title": "동물",
  "subjects": [
    "호랑이",
    "코끼리", 
    "펭귄",
    "기린",
    "토끼"
  ],
  "before_subjects": ["고양이", "강아지"],
  "difficulty": "medium"
}
```

**응답 필드**:
- `title` (string): 요청한 대주제
- `subjects` (array): 생성된 세부 주제 목록
- `before_subjects` (array): 이전 주제들
- `difficulty` (string): 적용된 난이도

**사용 예시**:
```bash
curl -X POST "http://localhost:8000/game_subjects" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "음식",
    "number": 3,
    "difficulty": "easy"
  }'
```

### 🔧 난이도 설명

| 난이도 | 설명 | 예시 |
|--------|------|------|
| `easy` | 일상생활에서 자주 접하는 기본적인 것들 | 고양이, 사과, 자동차 |
| `medium` | 적당한 인지도를 가진 표준적인 것들 | 기린, 아보카도, 헬리콥터 |
| `hard` | 좀 더 세분화되거나 전문적인 것들 | 카멜레온, 두리안, 잠수함 |

### ⚠️ 오류 응답

모든 엔드포인트에서 발생할 수 있는 일반적인 오류:

**400 Bad Request**:
```json
{
  "detail": "요청 데이터가 올바르지 않습니다"
}
```

**500 Internal Server Error**:
```json
{
  "detail": "서버 내부 오류가 발생했습니다"
}
```

### 💡 사용 팁

1. **게임 타이틀 추천**: 먼저 `/game_titles`로 대주제를 받은 후, 선택한 주제로 `/game_subjects`를 호출
2. **중복 방지**: `excluded_titles`와 `before_subjects`를 활용하여 중복된 추천 방지
3. **난이도 조절**: 사용자 수준에 맞게 `difficulty` 매개변수 조정
4. **배치 처리**: 여러 주제가 필요한 경우 `number` 매개변수로 한 번에 요청

## 🚀 실행 방법 및 사용 예시

### 🏃‍♂️ 서버 실행 방법

#### 방법 1: Python 직접 실행
```bash
# 가상환경 활성화
source .venv/bin/activate  # macOS/Linux
# 또는
.venv\Scripts\activate     # Windows

# 서버 실행
python main.py
```

#### 방법 2: uvicorn 명령어 사용
```bash
# 기본 실행
uvicorn main:app --reload

# 호스트와 포트 지정
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# 프로덕션 모드 (reload 없이)
uvicorn main:app --host 0.0.0.0 --port 8000
```

#### 방법 3: 백그라운드 실행
```bash
# nohup을 사용한 백그라운드 실행
nohup python main.py > server.log 2>&1 &

# 또는 uvicorn 사용
nohup uvicorn main:app --host 0.0.0.0 --port 8000 > server.log 2>&1 &
```

### 🌐 서버 접속 확인

서버가 정상적으로 실행되면 다음 URL에서 확인할 수 있습니다:
- **로컬 접속**: http://localhost:8000
- **네트워크 접속**: http://your-ip:8000
- **API 문서**: http://localhost:8000/docs (FastAPI 자동 생성)

### 📝 실제 사용 시나리오

#### 시나리오 1: 캐치마인드 게임 준비

**1단계: 게임 대주제 받기**
```bash
curl -X GET "http://localhost:8000/game_titles?number=3"
```

**응답 예시:**
```json
{
  "titles": ["동물", "음식", "교통수단"]
}
```

**2단계: 선택한 주제의 세부 항목 받기**
```bash
curl -X POST "http://localhost:8000/game_subjects" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "동물",
    "number": 5,
    "difficulty": "easy"
  }'
```

**응답 예시:**
```json
{
  "title": "동물",
  "subjects": ["고양이", "강아지", "토끼", "사자", "코끼리"],
  "before_subjects": [],
  "difficulty": "easy"
}
```

**3단계: 추가 라운드 (중복 방지)**
```bash
curl -X POST "http://localhost:8000/game_subjects" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "동물",
    "number": 5,
    "before_subjects": ["고양이", "강아지", "토끼", "사자", "코끼리"],
    "difficulty": "medium"
  }'
```

#### 시나리오 2: 웹 애플리케이션에서 사용

**JavaScript 예시:**
```javascript
// 게임 타이틀 가져오기
async function getGameTitles() {
  try {
    const response = await fetch('http://localhost:8000/game_titles?number=5');
    const data = await response.json();
    console.log('게임 타이틀:', data.titles);
    return data.titles;
  } catch (error) {
    console.error('오류:', error);
  }
}

// 게임 주제 가져오기
async function getGameSubjects(title, difficulty = 'medium') {
  try {
    const response = await fetch('http://localhost:8000/game_subjects', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        title: title,
        number: 5,
        difficulty: difficulty
      })
    });
    const data = await response.json();
    console.log('게임 주제:', data.subjects);
    return data.subjects;
  } catch (error) {
    console.error('오류:', error);
  }
}

// 사용 예시
getGameTitles().then(titles => {
  if (titles && titles.length > 0) {
    getGameSubjects(titles[0], 'easy');
  }
});
```

**Python 클라이언트 예시:**
```python
import requests
import json

# 서버 URL
BASE_URL = "http://localhost:8000"

def get_game_titles(number=5, excluded_titles=None):
    """게임 타이틀 가져오기"""
    params = {"number": number}
    if excluded_titles:
        params["excluded_titles"] = excluded_titles
    
    response = requests.get(f"{BASE_URL}/game_titles", params=params)
    return response.json()

def get_game_subjects(title, number=5, before_subjects=None, difficulty="medium"):
    """게임 주제 가져오기"""
    data = {
        "title": title,
        "number": number,
        "difficulty": difficulty
    }
    if before_subjects:
        data["before_subjects"] = before_subjects
    
    response = requests.post(
        f"{BASE_URL}/game_subjects",
        headers={"Content-Type": "application/json"},
        data=json.dumps(data)
    )
    return response.json()

# 사용 예시
if __name__ == "__main__":
    # 1. 게임 타이틀 받기
    titles_response = get_game_titles(number=3)
    print("게임 타이틀:", titles_response["titles"])
    
    # 2. 첫 번째 타이틀로 주제 받기
    if titles_response["titles"]:
        subjects_response = get_game_subjects(
            title=titles_response["titles"][0],
            number=5,
            difficulty="easy"
        )
        print("게임 주제:", subjects_response["subjects"])
```

### 🔧 실행 시 주의사항

1. **환경 변수 확인**: `.env` 파일에 `OPENAI_API_KEY`가 설정되어 있는지 확인
2. **포트 충돌**: 8000번 포트가 이미 사용 중인 경우 다른 포트 사용
3. **방화벽**: 외부 접속이 필요한 경우 방화벽 설정 확인
4. **API 키 한도**: OpenAI API 사용량 및 요금 확인

### 🐛 문제 해결

#### 서버가 시작되지 않는 경우
```bash
# 포트 사용 확인
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# 환경 변수 확인
python -c "import os; print(os.getenv('OPENAI_API_KEY'))"
```

#### API 호출 오류
```bash
# 서버 상태 확인
curl -X GET "http://localhost:8000/"

# 로그 확인
tail -f server.log  # 백그라운드 실행 시
```

#### CORS 오류 (웹에서 호출 시)
- 허용된 도메인 목록 확인: `localhost:8080`, `localhost:8443`, `hjproject.kro.kr`
- 다른 도메인에서 접속 시 `main.py`의 CORS 설정 수정 필요

### 📊 성능 최적화

#### 프로덕션 환경 설정
```bash
# Gunicorn 사용 (권장)
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

# 또는 uvicorn 워커 수 증가
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

#### 로그 설정
```python
# main.py에 로깅 추가 예시
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

## 🐳 Docker 사용법 및 배포

### 📦 Docker 이미지 빌드

#### 로컬 빌드
```bash
# 기본 빌드
docker build -t chatforyou-python-api .

# 태그 지정 빌드
docker build -t chatforyou-python-api:latest .
docker build -t chatforyou-python-api:v1.0.0 .
```

#### 멀티 플랫폼 빌드 (선택사항)
```bash
# ARM64와 AMD64 지원
docker buildx build --platform linux/amd64,linux/arm64 -t chatforyou-python-api:latest .
```

### 🚀 Docker 컨테이너 실행

#### 기본 실행
```bash
# 포트 매핑으로 실행
docker run -p 8000:8000 chatforyou-python-api

# 백그라운드 실행
docker run -d -p 8000:8000 --name chatforyou-api chatforyou-python-api
```

#### 환경 변수와 함께 실행
```bash
# 환경 변수 직접 지정
docker run -p 8000:8000 \
  -e OPENAI_API_KEY=your_api_key_here \
  chatforyou-python-api

# .env 파일 사용
docker run -p 8000:8000 \
  --env-file .env \
  chatforyou-python-api
```

#### 볼륨 마운트 (로그 저장)
```bash
# 로그 디렉토리 마운트
docker run -p 8000:8000 \
  -v $(pwd)/logs:/app/logs \
  --env-file .env \
  chatforyou-python-api
```

### 🔧 Docker Compose 사용

#### docker-compose.yml 파일 생성
```yaml
version: '3.8'

services:
  chatforyou-api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    env_file:
      - .env
    volumes:
      - ./logs:/app/logs
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  # 선택사항: Nginx 리버스 프록시
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - chatforyou-api
    restart: unless-stopped
```

#### Docker Compose 실행
```bash
# 서비스 시작
docker-compose up -d

# 로그 확인
docker-compose logs -f chatforyou-api

# 서비스 중지
docker-compose down

# 이미지 재빌드 후 시작
docker-compose up -d --build
```

### 🌐 배포 환경

#### GitHub Container Registry 사용
프로젝트는 GitHub Actions를 통해 자동으로 빌드되고 배포됩니다.

**자동 배포 워크플로우:**
1. `main` 브랜치에 푸시 시 자동 트리거
2. Docker 이미지 빌드
3. GitHub Container Registry에 푸시
4. Kubernetes 클러스터에 자동 배포

### 🔄 CI/CD 파이프라인

현재 프로젝트는 GitHub Actions를 통한 자동 배포가 설정되어 있습니다:

1. **트리거**: `main` 브랜치 푸시
2. **빌드**: Docker 이미지 생성
3. **푸시**: GitHub Container Registry에 업로드
4. **배포**: Kubernetes 클러스터에 자동 배포
5. **검증**: 배포 상태 확인

배포 상태는 GitHub Actions 탭에서 확인할 수 있습니다.

## 🤝 기여하기

ChatForYou 프로젝트에 기여해 주셔서 감사합니다! 다음과 같은 방법으로 기여할 수 있습니다:

### 🐛 버그 리포트
- GitHub Issues에 버그 리포트 작성
- 재현 가능한 단계와 예상 결과 포함
- 환경 정보 (OS, Python 버전 등) 명시

### 💡 기능 제안
- 새로운 기능에 대한 아이디어 제안
- 사용 사례와 구현 방안 설명
- 기존 기능과의 호환성 고려

### 🔧 코드 기여
1. 프로젝트 포크
2. 기능 브랜치 생성 (`git checkout -b feature/amazing-feature`)
3. 변경사항 커밋 (`git commit -m 'Add amazing feature'`)
4. 브랜치에 푸시 (`git push origin feature/amazing-feature`)
5. Pull Request 생성

### 📝 문서 개선
- README 개선
- API 문서 보완
- 코드 주석 추가

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

## 🙏 Thanks To

### 프롬프트 작성 및 제작에 도움
**HJH** :: h01068289030@gmail.com

---

**ChatForYou Python API Server** - AI 기반 게임 콘텐츠 추천 서비스

Made with ❤️ by Sejonj