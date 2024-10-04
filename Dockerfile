FROM python:3.12.5-alpine3.19

EXPOSE 5000

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

CMD ["python","app.py"]