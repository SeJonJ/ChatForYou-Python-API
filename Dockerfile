# Dockerfile (수정 버전)
FROM python:3.11.6

# 1. 의존성 먼저 설치 (레이어 캐싱 최적화)
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 2. 소스 코드 복사
WORKDIR /app
COPY . .

# 3. 실행 명령
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]