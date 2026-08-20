from django.db import models
from django.contrib.auth.models import User
from companies.models import CompanyProfile

class VehicleDetails(models.Model):
    brand = models.CharField(max_length=100)
    manufacturing_year = models.PositiveIntegerField()
    market_price = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        verbose_name_plural = "Vehicle Details"
        unique_together = ('brand', 'manufacturing_year')


    def __str__(self):
        return f"{self.brand} ({self.manufacturing_year})"

class ClaimRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    insurance_company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE)
    vehicle_details = models.ForeignKey(VehicleDetails, on_delete=models.CASCADE)
    vehicle_number = models.CharField(max_length=20)
    accident_date = models.DateField()
    accident_image = models.ImageField(upload_to='accident_images/')
    annotated_image = models.ImageField(upload_to='annotated_images/', blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Claim #{self.id} - {self.vehicle_number}"


class DamageDetection(models.Model):
    SEVERITY_CHOICES = [
        ('no_damage', 'No Damage'),
        ('minor', 'Minor Damage'),
        ('moderate', 'Moderate Damage'),
        ('major', 'Major Damage'),
    ]
    claim = models.ForeignKey(ClaimRequest, on_delete=models.CASCADE, related_name='detections')
    part_name = models.CharField(max_length=50)
    yolo_confidence = models.FloatField()
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES)
    severity_confidence = models.FloatField()
    bbox_x1 = models.FloatField()
    bbox_y1 = models.FloatField()
    bbox_x2 = models.FloatField()
    bbox_y2 = models.FloatField()

    def __str__(self):
        return f"{self.part_name} - {self.severity}"


class ClaimReport(models.Model):
    claim = models.OneToOneField(ClaimRequest, on_delete=models.CASCADE)
    claim_amount = models.DecimalField(max_digits=12, decimal_places=2)
    generated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report for Claim #{self.claim.id}"
