FROM python:3.10

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 9002

CMD ["python", "manage.py", "runserver", "0.0.0.0:9002"]
