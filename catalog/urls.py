from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),  # Home page
    path('signup/', views.signup, name='signup'),  # Signup page
    path('thank-you/', views.thank_you, name='thank_you'),  # Thank you page
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),  # Admin page
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('export-subscribers/', views.export_subscribers_csv, name='export_subscribers'),
    path('delete-subscriber/<int:subscriber_id>/', views.delete_subscriber, name='delete_subscriber'),
]
