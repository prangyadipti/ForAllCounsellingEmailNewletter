from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.http import HttpResponse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives, get_connection
from django.conf import settings
from smtplib import SMTPException
import csv
import logging

from .forms import SubscriberForm, NewsletterForm
from .models import Subscriber, Newsletter

# ----------------------------------------------------------------------------
# Module‑level constants & logger
# ----------------------------------------------------------------------------
DEFAULT_FROM = getattr(settings, "DEFAULT_FROM_EMAIL", "no-reply@example.com")
logger = logging.getLogger(__name__)

# ----------------------------------------------------------------------------
# Public Views
# ----------------------------------------------------------------------------

def home(request):
    """Public landing page."""
    return render(request, "home.html")


def signup(request):
    """Handle newsletter sign‑up and send welcome e‑mail."""
    if request.method == "POST":
        form = SubscriberForm(request.POST)
        if form.is_valid():
            subscriber = form.save()
            _send_welcome_email(subscriber)
            return redirect("thank_you")
    else:
        form = SubscriberForm()

    return render(request, "signup.html", {"form": form})


def thank_you(request):
    return render(request, "thank_you.html")


def newsletter_detail(request, pk):
    newsletter = get_object_or_404(Newsletter, pk=pk)
    return render(request, "newsletter_detail.html", {"newsletter": newsletter})


def logout_view(request):
    """End user session then return to home page."""
    logout(request)
    return redirect("home")

# ----------------------------------------------------------------------------
# Admin‑only Views
# ----------------------------------------------------------------------------

@login_required
def admin_dashboard(request):
    subscribers = Subscriber.objects.all()
    now = timezone.now()
    context = {
        "subscribers": subscribers,
        "total_subscribers": subscribers.count(),
        "current_month_signups": subscribers.filter(
            signup_date__year=now.year,
            signup_date__month=now.month,
        ).count(),
    }
    return render(request, "admin_dashboard.html", context)


@login_required
def export_subscribers_csv(request):
    """Stream subscribers as CSV download."""
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="subscribers.csv"'

    writer = csv.writer(response)
    writer.writerow(["First Name", "Last Name", "Email", "Company", "Signup Date"])
    for sub in Subscriber.objects.iterator():
        writer.writerow([
            sub.first_name,
            sub.last_name,
            sub.email,
            sub.company_name,
            sub.signup_date,
        ])

    return response


@login_required
def delete_subscriber(request, subscriber_id):
    get_object_or_404(Subscriber, pk=subscriber_id).delete()
    messages.success(request, "Subscriber deleted successfully.")
    return redirect("admin_dashboard")


@login_required
def add_newsletter(request):
    if request.method == "POST":
        form = NewsletterForm(request.POST)
        if form.is_valid():
            nl = form.save()
            messages.success(request, f'Newsletter “{nl.title}” created.')
            return redirect("newsletter_admin")
    else:
        form = NewsletterForm()

    return render(request, "add_newsletter.html", {"form": form})


@login_required
def newsletter_admin(request):
    """List newsletters and perform bulk actions (send / delete)."""
    if request.method == "POST":
        action = request.POST.get("action")
        selected_ids = request.POST.getlist("selected_newsletters")

        if not action or not selected_ids:
            messages.error(request, "Choose an action and at least one newsletter.")
            return redirect("newsletter_admin")

        newsletters = Newsletter.objects.filter(id__in=selected_ids)
        count = newsletters.count()

        if action == "send":
            _bulk_send_newsletters(newsletters)
            newsletters.update(is_sent=True)
            verb = "Sent"
        elif action == "delete":
            newsletters.delete()
            verb = "Deleted"
        else:
            messages.error(request, "Unknown action.")
            return redirect("newsletter_admin")

        messages.success(request, f"{verb} {count} newsletter{'s' if count != 1 else ''}.")
        return redirect("newsletter_admin")

    context = {"newsletters": Newsletter.objects.all().order_by("-created_at")}
    return render(request, "newsletter_admin.html", context)

# ----------------------------------------------------------------------------
# Helper functions (private)
# ----------------------------------------------------------------------------

def _send_welcome_email(subscriber):
    """Send a single HTML + plain‑text welcome e‑mail."""
    html = render_to_string("welcome_email.html", {"subscriber": subscriber})
    text = strip_tags(html)

    email = EmailMultiAlternatives(
        subject="Welcome to For All Counseling!",
        body=text,
        from_email=DEFAULT_FROM,
        to=[subscriber.email],
    )
    email.attach_alternative(html, "text/html")

    try:
        email.send(fail_silently=False)
    except SMTPException:
        logger.exception("Failed to send welcome email to %s", subscriber.email)


def _bulk_send_newsletters(newsletters):
    """Send each newsletter to **all** subscribers using one SMTP connection."""
    subscriber_emails = list(Subscriber.objects.values_list("email", flat=True))
    if not subscriber_emails:
        return

    connection = get_connection()
    emails = []

    for nl in newsletters:
        for addr in subscriber_emails:
            html = render_to_string(
                "newsletter_email.html",
                {"subscriber_email": addr, "newsletter": nl},
            )
            msg = EmailMultiAlternatives(
                subject=nl.title,
                body=strip_tags(html),
                from_email=DEFAULT_FROM,
                to=[addr],
                connection=connection,
            )
            msg.attach_alternative(html, "text/html")
            emails.append(msg)

    connection.send_messages(emails)
    connection.close()
