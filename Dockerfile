FROM python:3.9-slim
WORKDIR /app

RUN apt-get update && \
    apt-get install -y libjpeg-dev zlib1g-dev && \
    apt-get clean

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "discord-bot.py"]

