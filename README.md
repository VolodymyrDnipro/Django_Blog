### Django_Blog
```bash
pip install -r requirements.txt
```

```bash
python manage.py makemigrations
```

```bash
python manage.py migrate
```

```bash
docker compose up
```

```bash
python manage.py runserver
```

```bash
python manage.py createsuperuser
```
```bash
celery -A simple_blog worker -l info
```
```bash
flower -A simple_blog
```

### Before creating the PHOTO_PATH setting
```bash
python manage.py generate_posts 10 
```

```bash
python manage.py generate_comments 10
```