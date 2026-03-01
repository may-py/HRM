from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.db import transaction
from django.contrib import messages # Import this for the popup message
from .models import RecruiterProfile

class FreelancerSignUpView(CreateView):
    model = User
    fields = ['first_name', 'last_name', 'email', 'username']
    template_name = 'recruiter/freelancer_signup.html'
    success_url = reverse_lazy('login') # 🟢 Redirect to login instead of success page

    def form_valid(self, form):
        try:
            with transaction.atomic():
                # 1. Create the User
                user = form.save(commit=False)
                user.is_active = True # 🟢 Changed to True (No approval needed)
                # You'll likely want to add a password field to your form later, 
                # but for now, we'll keep your logic.
                user.set_password("Freelance2026!") 
                user.save()

                # 2. Create the Profile as a standalone individual
                RecruiterProfile.objects.create(
                    user=user,
                    company=None, 
                    is_freelancer=True
                )
                
                # 3. Add a success message
                messages.success(self.request, "Account created! You can now sign in.")
                
            return super().form_valid(form)
        except Exception as e:
            form.add_error(None, f"Registration failed: {e}")
            return self.form_invalid(form)