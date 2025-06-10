FROM python:3.9-slim

ENV TZ=Asia/Tokyo \
    LANG=ja_JP.UTF-8 \
    LANGUAGE=ja_JP:ja \
    LC_ALL=ja_JP.UTF-8

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    locales vim less && \
    localedef -f UTF-8 -i ja_JP ja_JP.UTF-8 && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip setuptools && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "opt/app.py"]
