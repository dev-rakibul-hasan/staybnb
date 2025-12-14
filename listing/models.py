from django.db import models
from accounts.models import User

class Listing(models.Model):
    host = models.ForeignKey(User, on_delete = models.CASCADE)

    title = models.CharField(max_length = 200)
    description = models.TextField()
    address = models.CharField(max_length = 255)
    city = models.CharField(max_length = 100)
    country = models.CharField(max_length = 100)

    price_per_night = models.IntegerField()
    max_guests = models.IntegerField()

    image = models.ImageField(upload_to = 'listing_images/', null = True, blank = True)

    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.title
