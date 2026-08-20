from django.db import models
from django.contrib.auth.models import User

class CompanyProfile(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=200)
    license_number = models.CharField(max_length=100, unique=True)
    mobile_number = models.CharField(max_length=15)
    city = models.CharField(max_length=100)
    office_address = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return self.company_name
    
