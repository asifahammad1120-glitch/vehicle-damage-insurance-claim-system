from django.contrib import admin
from .models import VehicleDetails, ClaimRequest, DamageDetection, ClaimReport

admin.site.register(VehicleDetails)
admin.site.register(ClaimRequest)
admin.site.register(DamageDetection)
admin.site.register(ClaimReport)