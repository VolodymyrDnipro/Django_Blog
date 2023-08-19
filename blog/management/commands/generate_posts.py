from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from faker import Faker
from blog.models import Post
from django.core.files import File
from dotenv import load_dotenv
from envparse import Env

load_dotenv()
env = Env()


class Command(BaseCommand):
    help = 'Generate random blog posts'

    def add_arguments(self, parser):
        parser.add_argument('count', type=int, help='Indicates the number of posts to be created')

    def handle(self, *args, **kwargs):
        fake = Faker()
        count = kwargs['count']

        User = get_user_model()
        superuser = User.objects.get(username='admin')

        for _ in range(count):
            title = fake.sentence()
            short_description = fake.text()
            content = fake.paragraph()
            draft = False
            post = Post(title=title, is_draft=draft, short_description=short_description, content=content, owner=superuser)

            image_path = env.str('PHOTO_PATH')
            with open(image_path, 'rb') as f:
                post.image.save('photo.jpg', File(f), save=True)

            post.save()

        self.stdout.write(self.style.SUCCESS(f'Successfully generated {count} posts'))
