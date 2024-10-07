FROM python:3.10

WORKDIR /app

RUN python3 -m pip install rasa==3.5.0

COPY requirements.txt .

## --no-cache-dir 
RUN pip install -r requirements.txt

RUN python -m pip install -U channels["daphne"]
COPY . .

EXPOSE 9002

ENV DATABASE_URL=postgres://postgres:Intern2024@db:5432/amaz_ai_chatbot

CMD ["python", "manage.py", "runserver", "0.0.0.0:9002"]
