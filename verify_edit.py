import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from listing.models import Listing
from accounts.models import User

# Get the user
user = User.objects.get(email="host_manual_test_v2@test.com")

# Get the listing
listing = Listing.objects.filter(host=user).first()

if listing:
    print(f"Original Title: {listing.title}")
    print(f"Original Price: {listing.price_per_night}")
    
    # Simulate edit
    listing.title = "Verified Edit House Script"
    listing.price_per_night = 300
    listing.save()
    
    # Verify
    updated_listing = Listing.objects.get(id=listing.id)
    print(f"Updated Title: {updated_listing.title}")
    print(f"Updated Price: {updated_listing.price_per_night}")
    
    if updated_listing.title == "Verified Edit House Script" and updated_listing.price_per_night == 300:
        print("SUCCESS: Listing updated successfully.")
    else:
        print("FAILURE: Listing update failed.")
else:
    print("No listing found for this user.")
