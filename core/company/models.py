from django.db import models
from core.models import TimeStampedModel
from auditlog.registry import auditlog  




class Company(TimeStampedModel):
    name = models.CharField(max_length=255, unique=True)
    website = models.URLField(blank=True)
    location = models.CharField(max_length=255, default="Vietnam")
    is_verified = models.BooleanField(default=True) # Usually true if approved via request
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

auditlog.register(Company)

class CompanyRequest(TimeStampedModel):
    STATUS_CHOICES = (
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    # Basic Info
    company_name = models.CharField(max_length=255)
    business_license_id = models.CharField(max_length=100, unique=True, help_text="MST in Vietnam")
    website = models.URLField()
    
    # Contact Person (The one who will become the first Recruiter user)
    contact_name = models.CharField(max_length=255)
    contact_email = models.EmailField(unique=True)
    contact_phone = models.CharField(max_length=20)
    
    # Status & Admin notes
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    admin_notes = models.TextField(blank=True, help_text="Internal notes on why they were approved/rejected")

    def __str__(self):
        return f"{self.company_name} ({self.get_status_display()})"
    
auditlog.register(CompanyRequest)