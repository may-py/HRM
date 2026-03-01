from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.db import transaction
from django.contrib import messages
from .forms import FreelancerRegistrationForm
from .models import RecruiterProfile
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

class FreelancerSignUpView(CreateView):
    form_class = FreelancerRegistrationForm # 🟢 Use the custom form
    template_name = 'recruiter/freelancer_signup.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        try:
            with transaction.atomic():
                # 1. Save the User (UserCreationForm handles hashing/is_active)
                user = form.save() 

                # 2. Create the standalone Profile
                RecruiterProfile.objects.create(
                    user=user,
                    company=None, 
                    is_freelancer=True
                )
                
                messages.success(self.request, "Account created successfully! Please sign in.")
                
            return super().form_valid(form)
        except Exception as e:
            messages.error(self.request, f"Error: {e}")
            return self.form_invalid(form)
        

@login_required
def freelancer_dashboard(request):
    # Ensure only freelancers can see this
    if not request.user.recruiter_profile.is_freelancer:
        return redirect('company:dashboard')
        
    return render(request, 'recruiter/dashboard.html', {
        'profile': request.user.recruiter_profile
    })