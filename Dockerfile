FROM python:3.11.6
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
COPY .env /app/.env
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]