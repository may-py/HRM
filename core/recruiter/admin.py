from django.contrib import admin
from .models import RecruiterProfile

# Register your models here.

@admin.register(RecruiterProfile)
class RecruiterProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_company_status', 'is_freelancer', 'created_at')
    list_filter = ('is_freelancer', 'company', 'created_at')
    search_fields = ('user__email', 'company__name', 'tax_code')

    def get_company_status(self, obj):
        return obj.company.name if obj.company else "Independent"
    get_company_status.short_description = 'Affiliation'