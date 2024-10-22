FROM python:3.10

WORKDIR /app

COPY . /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 9002


ENV DATABASE_URL=postgres://postgres:Intern2024@db:5432/amaz_ai_chatbot


CMD ["python", "manage.py", "runserver", "0.0.0.0:9002"]
