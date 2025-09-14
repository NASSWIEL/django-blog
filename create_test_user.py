import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')
django.setup()

from django.contrib.auth.models import User

# Create a test user if it doesn't exist
def create_test_user():
    username = 'asswiel_nayef'
    email = 'asswiel_nayef@gmail.com'
    
    if not User.objects.filter(username=username).exists():
        user = User.objects.create_user(
            username=username,
            email=email,
            password='testpass123'
        )
        print(f"Created test user: {user.username}")
        print(f"Email: {user.email}")
        print(f"Password: testpass123")
        
        # Check if profile was created by signal
        if hasattr(user, 'profile'):
            print(f"Profile created: {user.profile}")
        else:
            print("Profile not found - signals might not be working")
    else:
        print(f"User {username} already exists")

if __name__ == '__main__':
    create_test_user()