from django.db import models
from django.contrib.auth.models import User
from core.models import TimeStampedModel
from auditlog.registry import auditlog

class SeekerProfile(TimeStampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='seeker_profile')
    phone = models.CharField(max_length=20, blank=True)
    bio = models.TextField(blank=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    skills = models.TextField(help_text="Enter skills separated by commas")

    def __str__(self):
        return f"Seeker: {self.user.username}"

# Don't forget to register with auditlog!
auditlog.register(SeekerProfile)