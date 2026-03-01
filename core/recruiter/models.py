from django.db import models
from django.contrib.auth.models import User
# Import the base model from your Core app
from core.models import TimeStampedModel
from auditlog.registry import auditlog  # 1. Import the registry



class RecruiterProfile(TimeStampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='recruiter_profile')
    # Allow null/blank so Freelancers don't need a Company
    company = models.ForeignKey(
        'company.Company', 
        on_delete=models.CASCADE, 
        related_name='recruiters',
        null=True, 
        blank=True
    )
    is_freelancer = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.is_freelancer:
            return f"Freelancer: {self.user.username}"
        return f"{self.user.username} - {self.company.name if self.company else 'No Company'}"
        
auditlog.register(RecruiterProfile)