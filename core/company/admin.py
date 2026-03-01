from django.contrib import admin
from .models import CompanyRequest
from auditlog.registry import auditlog

@admin.register(CompanyRequest)
class CompanyRequestAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'contact_name', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('company_name', 'business_license_id', 'contact_email')
    
    # We make status editable directly in the list to speed up onboarding
    list_editable = ('status',)

# Auditlog is crucial here to see who approved which company
auditlog.register(CompanyRequest)