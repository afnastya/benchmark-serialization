FROM python:3.10

WORKDIR /app

COPY . .

RUN python3 -m venv venv
RUN . venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt

CMD . venv/bin/activate && exec python proxy.py
