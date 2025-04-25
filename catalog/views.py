from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.contrib import messages
from django.http import HttpResponse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
import csv

from .forms import SubscriberForm, NewsletterForm
from .models import Subscriber, Newsletter


# ─── Home Page ────────────────────────────────────────────────
def home(request):
    return render(request, 'home.html')


# ─── Signup Page + Welcome Email ──────────────────────────────
def signup(request):
    if request.method == 'POST':
        form = SubscriberForm(request.POST)
        if form.is_valid():
            subscriber = form.save()

            # Build and send welcome email
            html_content = render_to_string('welcome_email.html', {
                'subscriber': subscriber
            })
            text_content = strip_tags(html_content)
            email = EmailMultiAlternatives(
                subject="Welcome to For All Counseling!",
                body=text_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[subscriber.email],
            )
            email.attach_alternative(html_content, "text/html")
            email.send()

            return redirect('thank_you')
    else:
        form = SubscriberForm()
    return render(request, 'signup.html', {'form': form})


# ─── Thank You Page ───────────────────────────────────────────
def thank_you(request):
    return render(request, 'thank_you.html')


# ─── Admin Dashboard ──────────────────────────────────────────
@login_required
def admin_dashboard(request):
    subscribers = Subscriber.objects.all()
    total = subscribers.count()
    now = timezone.now()
    this_month = subscribers.filter(
        signup_date__year=now.year,
        signup_date__month=now.month
    ).count()
    return render(request, 'admin_dashboard.html', {
        'subscribers': subscribers,
        'total_subscribers': total,
        'current_month_signups': this_month,
    })


# ─── Export Subscribers to CSV ────────────────────────────────
@login_required
def export_subscribers_csv(request):
    subscribers = Subscriber.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="subscribers.csv"'
    writer = csv.writer(response)
    writer.writerow(['First Name', 'Last Name', 'Email', 'Company', 'Signup Date'])
    for s in subscribers:
        writer.writerow([s.first_name, s.last_name, s.email, s.company_name, s.signup_date])
    return response


# ─── Delete Subscriber ────────────────────────────────────────
@login_required
def delete_subscriber(request, subscriber_id):
    sub = get_object_or_404(Subscriber, id=subscriber_id)
    sub.delete()
    messages.success(request, "Subscriber deleted successfully.")
    return redirect('admin_dashboard')


# ─── Public Newsletter Detail Page ────────────────────────────
def newsletter_detail(request, pk):
    nl = get_object_or_404(Newsletter, pk=pk)
    return render(request, 'newsletter_detail.html', {'newsletter': nl})


# ─── Log Out ──────────────────────────────────────────────────
def logout_view(request):
    logout(request)
    return render(request, 'logout.html')


# ─── Add Newsletter ───────────────────────────────────────────
@login_required
def add_newsletter(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            nl = form.save(commit=False)
            nl.save()
            messages.success(request, f'Newsletter “{nl.title}” created.')
            return redirect('newsletter_admin')
    else:
        form = NewsletterForm()
    return render(request, 'add_newsletter.html', {'form': form})


# ─── Newsletter Admin – Send/Delete/Manage ───────────────────
@login_required
def newsletter_admin(request):
    if request.method == 'POST':
        action = request.POST.get('action', '')
        selected = request.POST.getlist('selected_newsletters')
        if not action or not selected:
            messages.error(request, "Choose an action and at least one newsletter.")
        else:
            count = 0
            for nid in selected:
                n = get_object_or_404(Newsletter, id=nid)
                if action == 'send':
                    # Send newsletter to all subscribers
                    subscribers = Subscriber.objects.all()
                    for subscriber in subscribers:
                        html_content = render_to_string('newsletter_email.html', {
                            'subscriber': subscriber,
                            'newsletter': n
                        })
                        text_content = strip_tags(html_content)
                        email = EmailMultiAlternatives(
                            subject=n.title,
                            body=text_content,
                            from_email=settings.DEFAULT_FROM_EMAIL,
                            to=[subscriber.email],
                        )
                        email.attach_alternative(html_content, "text/html")
                        email.send()
                    n.is_sent = True
                    n.save()
                elif action == 'delete':
                    n.delete()
                count += 1
            verb = "Sent" if action == 'send' else "Deleted"
            messages.success(request, f"{verb} {count} newsletter{'s' if count!=1 else ''}.")
        return redirect('newsletter_admin')

    newsletters = Newsletter.objects.all().order_by('-created_at')
    return render(request, 'newsletter_admin.html', {'newsletters': newsletters})