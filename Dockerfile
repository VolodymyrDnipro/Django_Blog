FROM python:3.10
WORKDIR /app

COPY .env requirements.txt /app/

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app

EXPOSE 8000

CMD ["python", "main.py"]
CMD ["pytest"]