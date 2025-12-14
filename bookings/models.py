from django.db import models
from accounts.models import User
from listing.models import Listing

class Booking(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    )

    guest = models.ForeignKey(User, on_delete = models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete = models.CASCADE)

    check_in = models.DateField()
    check_out = models.DateField()
    total_price = models.IntegerField()

    status = models.CharField(max_length = 10, choices = STATUS_CHOICES, default = 'pending')
    is_paid = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f"{self.guest.email} -> {self.listing.title}"

    @property
    def nights(self):
        return (self.check_out - self.check_in).days
