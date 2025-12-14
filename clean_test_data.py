import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from accounts.models import User
from django.db.models import Q

# Users to delete by email or phone
criteria = Q(email__in=['guest_browser@test.com', 'guest_browser_2@test.com', 'testuser@test.com', 'guestuser@test.com']) | \
           Q(phone__in=['1234567890', '1122334455'])

count, _ = User.objects.filter(criteria).delete()
print(f"Deleted {count} user(s) matching criteria.")
print("Cleanup complete.")
