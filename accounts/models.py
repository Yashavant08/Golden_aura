from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

class Profile(models.Model):
    GENDER_CHOICES = [
        ('Women', 'Women'),
        ('Men', 'Men'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile_number = models.CharField(max_length=15)
    address = models.TextField()
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, null=True, blank=True)

    def __str__(self):
        return self.user.username




class PasswordResetOTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    def is_expired(self):
        # OTP 10 minute mein expire ho jayega
        return timezone.now() > self.created_at + timedelta(minutes=10)

    def __str__(self):
        return f"OTP for {self.user.email} - {self.otp}"