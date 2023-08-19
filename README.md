## Django Blog Setup Guide
### This guide will help you set up the Django Blog project on your local machine. Make sure you have Python, Celery and Docker installed.

#### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```
#### Step 2: Set Up Environment Variables.
Create a .env file in the project root directory and add the following variables.
#### Step 3: Apply Migrations
```bash
python manage.py makemigrations
```
```bash
python manage.py migrate
```

#### Step 4: Run Docker Compose

```bash
docker compose up
```

#### Step 5: Run the Development Server
```bash
python manage.py runserver
```

#### Step 6: Create Superuser
```bash
python manage.py createsuperuser
```

#### Step 7: Start Celery Worker
```bash
celery -A simple_blog worker -l info
```

#### Step 8: Start Flower Monitoring Tool (Optional)
```bash
flower -A simple_blog
```

#### Step 9: Generate Sample Data (Optional)
After creating the PHOTO_PATH setting, generate sample posts and comments with the following commands:
```bash
python manage.py generate_posts 10 
```

```bash
python manage.py generate_comments 10
```

Now you're ready to explore and interact with your Django Blog application. Open your web browser and go to http://127.0.0.1:8000/ to access the blog. Use the Django admin interface to log in with the superuser account and manage the content.




