from django.shortcuts import render, redirect
from .forms import SubscriberForm
from .models import Subscriber


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
    return render(request, 'admin_dashboard.html', {'subscribers': subscribers})