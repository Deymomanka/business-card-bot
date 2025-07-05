FROM python:3.9

RUN apt-get update && \
    apt-get -qq -y install tesseract-ocr tesseract-ocr-jpn libtesseract-dev

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "-b", "0.0.0.0:10000", "-w", "1", "app.main:app"]

