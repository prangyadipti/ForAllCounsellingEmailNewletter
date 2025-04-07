from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Home page
    path('signup/', views.signup, name='signup'),  # Signup page
    path('thank-you/', views.thank_you, name='thank_you'),  # Thank you page
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),  # Admin page
]