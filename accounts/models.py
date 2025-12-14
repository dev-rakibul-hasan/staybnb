from django.db import models

# Create your models here.
class User(models.Model):
    ROLE_CHOICES = (
        ('guest', 'Guest'),
        ('host', 'Host'),
    )

    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, unique= True)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    failed_attempts = models.IntegerField(default=0)
    is_locked = models.BooleanField(default=False)
    lock_until = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
    
