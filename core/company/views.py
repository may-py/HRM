from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, DetailView
from .models import CompanyRequest, Company
from .forms import CompanyOnboardingForm
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages
from django.contrib.auth.models import User
from recruiter.models import RecruiterProfile
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction, IntegrityError  # <--- Add IntegrityError here


@login_required
def smart_redirect(request):
    # 1. Admins go to Management
    if request.user.is_superuser:
        return redirect('company:admin_dashboard')
    
    # 2. Check for Recruiter Profile
    profile = getattr(request.user, 'recruiter_profile', None)
    
    if profile:
        # It's a Recruiter (Freelance or Company)
        if profile.is_freelancer:
            return redirect('recruiter:freelancer_dashboard')
        return redirect('company:dashboard')
    
    # 3. If no RecruiterProfile, they are a Job Seeker
    return redirect('seeker:home')


class AdminDashboardView(UserPassesTestMixin, ListView):
    model = CompanyRequest
    template_name = 'company/admin_dashboard.html'
    context_object_name = 'requests'
    
    def test_func(self):
        return self.request.user.is_superuser

    def get_queryset(self):
        # Get the 'status' from the URL, default to 'pending'
        status_filter = self.request.GET.get('status', 'pending')
        return CompanyRequest.objects.filter(status=status_filter).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pass the current status to the template to change headings
        context['current_status'] = self.request.GET.get('status', 'pending')
        return context


class CompanyRequestDetailView(UserPassesTestMixin, DetailView):
    model = CompanyRequest
    template_name = 'company/request_detail.html'
    context_object_name = 'onboarding'

    def test_func(self):
        return self.request.user.is_superuser
    
    def post(self, request, *args, **kwargs):
        onboarding = self.get_object()
        action = request.POST.get('action')

        if action == 'approve' and onboarding.status == 'pending':
            try:
                with transaction.atomic():
                    # 1. Create Company
                    new_company = Company.objects.create(
                        name=onboarding.company_name,
                        website=onboarding.website,
                        is_verified=True
                    )
                    
                    # 2. Create/Get User
                    user, created = User.objects.get_or_create(
                        email=onboarding.contact_email,
                        defaults={
                            'username': onboarding.contact_email,
                            'first_name': onboarding.contact_name
                        }
                    )
                    
                    if created:
                        user.set_password("SecureTemp123!") 
                        user.save()

                    # 3. Create Recruiter Profile
                    RecruiterProfile.objects.create(
                        user=user,
                        company=new_company,
                        is_freelancer=False
                    )
                    
                    # 4. Update Request
                    onboarding.status = 'approved'
                    onboarding.save()
                    
                    messages.success(request, f"Confirmed: {new_company.name} is now active.")

            except IntegrityError:
                messages.error(request, "Database Conflict: This company or user email already exists.")
        
        elif action == 'reject':
            onboarding.status = 'rejected'
            onboarding.save()
            messages.info(request, "Request moved to Rejected status.")

        return redirect('company:admin_dashboard')


# The missing Landing View
class CompanyLandingView(TemplateView):
    template_name = 'company/landing.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Partner with HRs - Scale Your Team"
        return context

# The Form Submission View
class CompanyRequestView(CreateView):
    model = CompanyRequest
    form_class = CompanyOnboardingForm
    template_name = 'company/onboarding_form.html'
    success_url = reverse_lazy('company:request_success')

# The Post-Submission View
class RequestSuccessView(TemplateView):
    template_name = 'company/success.html'