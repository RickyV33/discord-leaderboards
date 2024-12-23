FROM python:3.12.5-alpine

WORKDIR /app

COPY requirements.txt /app/requirements.txt
COPY bot/ /app/bot/
COPY channels/ /app/channels/
COPY db/ /app/db/
COPY games/ /app/games/
COPY actions.py /app/actions.py
COPY app.py /app/app.py

ENV DB_NAME=${DB_NAME}
ENV DB_NAME=${DISCORD_TOKEN}


RUN pip install --upgrade pip && pip install -r requirements.txt

CMD python3 -u /app/app.py run
