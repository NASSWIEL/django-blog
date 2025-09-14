import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')
django.setup()

from django.contrib.auth.models import User
from blog.models import Post
from django.utils import timezone

def create_sample_posts():
    # Get or create a test user
    user, created = User.objects.get_or_create(
        username='testuser',
        defaults={
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User'
        }
    )
    if created:
        user.set_password('testpass123')
        user.save()
        print(f"Created user: {user.username}")
    else:
        print(f"Using existing user: {user.username}")

    # Create sample posts if they don't exist
    existing_posts = Post.objects.filter(author=user).count()
    if existing_posts < 15:
        posts_to_create = 15 - existing_posts
        for i in range(posts_to_create):
            post_num = existing_posts + i + 1
            Post.objects.create(
                title=f'Sample Post {post_num}',
                content=f'This is the content of sample post {post_num}. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.',
                author=user,
                date_posted=timezone.now()
            )
        print(f"Created {posts_to_create} sample posts for testing pagination")
    else:
        print("Sample posts already exist")

if __name__ == '__main__':
    create_sample_posts()
    print("Sample data creation completed!")