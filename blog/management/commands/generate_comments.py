from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from faker import Faker
from blog.models import Comment, Post

class Command(BaseCommand):
    help = 'Generate random comments for posts'

    def add_arguments(self, parser):
        parser.add_argument('count', type=int, help='Indicates the number of comments to be created')

    def handle(self, *args, **kwargs):
        fake = Faker()
        count = kwargs['count']

        User = get_user_model()
        superuser = User.objects.get(username='admin')

        posts = Post.objects.all()

        for post in posts:
            for _ in range(count):
                username = fake.user_name()
                text = fake.paragraph()
                is_published = True
                comment = Comment(
                    post=post,
                    username=username,
                    text=text,
                    is_published=is_published,
                )
                comment.save()

        self.stdout.write(self.style.SUCCESS(f'Successfully generated {count} comments for each post'))
