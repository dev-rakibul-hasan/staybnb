import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from accounts.models import User
from django.contrib.auth.hashers import make_password

email = 'guest_manual@example.com'
print(f"Attempting to create user: {email}")

try:
    if User.objects.filter(email=email).exists():
        print("User already exists, deleting...")
        User.objects.get(email=email).delete()

    user = User.objects.create(
        full_name='Guest Manual',
        email=email,
        phone='9998887777',
        password=make_password('password123'),
        role='guest'
    )
    print(f"User created successfully: {user.email}")
except Exception as e:
    print(f"Failed to create user: {e}")
