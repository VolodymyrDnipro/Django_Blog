FROM python:3.10
WORKDIR /app

COPY .env requirements.txt /app/

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app

# Add the path to the Django project directory to PYTHONPATH
ENV PYTHONPATH "${PYTHONPATH}:/app"

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
