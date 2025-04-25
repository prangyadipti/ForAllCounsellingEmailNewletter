from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # public pages
    path('',                    views.home,              name='home'),
    path('signup/',             views.signup,            name='signup'),
    path('thank-you/',          views.thank_you,         name='thank_you'),
    path('login/',  auth_views.LoginView.as_view(template_name='login.html'),
                                  name='login'),
    path('logout/',             views.logout_view,       name='logout'),

    # subscriber admin
    path('admin-dashboard/',    views.admin_dashboard,   name='admin_dashboard'),
    path('export-subscribers/', views.export_subscribers_csv, name='export_subscribers'),
    path('delete-subscriber/<int:subscriber_id>/',
                                views.delete_subscriber,   name='delete_subscriber'),

    # newsletter CRUD
    path('add-newsletter/',     views.add_newsletter,    name='add_newsletter'),
    path('newsletter-admin/',   views.newsletter_admin,  name='newsletter_admin'),

    # public “Read More” link
    path('newsletters/<int:pk>/', views.newsletter_detail, name='newsletter_detail'),
]