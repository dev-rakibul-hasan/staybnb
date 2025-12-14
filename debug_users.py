import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from accounts.models import User

emails = ['guest_test4@example.com', 'guest_test5@example.com', 'guest_test6@example.com']

print("Checking users...")
for email in emails:
    try:
        user = User.objects.get(email=email)
        print(f"User found: {user.email}, Role: {user.role}, Active: {user.is_active}")
    except User.DoesNotExist:
        print(f"User NOT found: {email}")

print("All users:")
for u in User.objects.all():
    print(f"- {u.email} ({u.role})")
