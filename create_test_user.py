import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from accounts.models import User

from django.contrib.auth.hashers import make_password

email = "host_manual_test_v2@test.com"
password = "password123"
import random
phone = str(random.randint(1000000000, 9999999999))

try:
    user = User.objects.get(email=email)
    print(f"User {email} already exists")
    user.password = make_password(password)
    user.save()
    print(f"Password updated for {email}")
except User.DoesNotExist:
    user = User.objects.create(
        email=email, 
        password=make_password(password), 
        full_name="Manual Host", 
        role="host",
        phone=phone
    )
    print(f"User {email} created")
