from django.urls import path
from .views import FreelancerSignUpView

app_name = 'recruiter'

urlpatterns = [
    path('join-as-freelancer/', FreelancerSignUpView.as_view(), name='freelancer_signup'),
    # We will add freelancer_dashboard here later

]