from django import forms
from .models import CompanyRequest

class CompanyOnboardingForm(forms.ModelForm):
    class Meta:
        model = CompanyRequest
        fields = [
            'company_name', 'business_license_id', 'website', 
            'contact_name', 'contact_email', 'contact_phone'
        ]
        # Adding CSS classes for a professional look (Bootstrap-ready)
        widgets = {
            field: forms.TextInput(attrs={'class': 'form-control'}) 
            for field in ['company_name', 'business_license_id', 'contact_name', 'contact_phone']
        }
    
        # Custom widget for email and website
        widgets['contact_email'] = forms.EmailInput(attrs={'class': 'form-control'})
        widgets['website'] = forms.URLInput(attrs={'class': 'form-control'})