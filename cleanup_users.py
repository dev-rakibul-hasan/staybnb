import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from accounts.models import User
User.objects.filter(email='host@test.com').delete()
User.objects.filter(email='guest@test.com').delete()
print("Deleted users")
