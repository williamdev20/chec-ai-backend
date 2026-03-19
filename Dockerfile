FROM python:3.10

WORKDIR /app

RUN apt-get update && apt-get install -y libgl1 libglib2.0-0t64 tesseract-ocr tesseract-ocr-por
COPY pyproject.toml uv.lock ./
COPY app ./app

RUN pip install --upgrade pip
RUN pip install uv

EXPOSE 8080

CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
