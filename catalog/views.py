from django.shortcuts import render, redirect
from .forms import SubscriberForm
from .models import Subscriber
from django.contrib.auth import logout
import csv
from django.http import HttpResponse
from django.utils import timezone

def home(request):
    return render(request, 'home.html')  # This will look for templates/home.html

def signup(request):
    if request.method == 'POST':
        form = SubscriberForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('thank_you')
    else:
        form = SubscriberForm()
    return render(request, 'signup.html', {'form': form})

def thank_you(request):
    return render(request, 'thank_you.html')


def admin_dashboard(request):
    subscribers = Subscriber.objects.all()
    total_subscribers = subscribers.count()


    now = timezone.now()
    current_month_signups = subscribers.filter(
        signup_date__year=now.year, signup_date__month=now.month
    ).count()      # Filter current month signups

    return render(request, 'admin_dashboard.html', {
        'subscribers': subscribers,
        'total_subscribers': total_subscribers,
        'current_month_signups': current_month_signups,
        })

def export_subscribers_csv(request):
    subscribers = Subscriber.objects.all()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="subscribers.csv"'

    writer = csv.writer(response)
    writer.writerow(['First Name', 'Last Name', 'Email', 'Company', 'Signup Date'])

    for s in subscribers:
        writer.writerow([s.first_name, s.last_name, s.email, s.company_name, s.signup_date])

    return response


def delete_subscriber(request, subscriber_id):
    subscriber = get_object_or_404(Subscriber, id=subscriber_id)
    subscriber.delete()
    messages.success(request, "Subscriber deleted successfully.")
    return redirect('admin_dashboard')


def logout_view(request):
    logout(request)  # Logs out the user
    return render(request, 'logout.html')  # Renders the template
