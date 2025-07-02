FROM python:3.9

WORKDIR /app
COPY . /app

RUN apt-get update && \
    apt-get install -y tesseract-ocr

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["python", "app/main.py"]
