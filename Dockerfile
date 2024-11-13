FROM python:3.12.5-alpine

WORKDIR /app

COPY . /app/

RUN pip install --upgrade pip && pip install -r requirements.txt

CMD python3 -u /app/discord_leaderboards/app.py
