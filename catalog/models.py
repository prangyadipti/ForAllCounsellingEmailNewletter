from django.db import models


# ────────────────────────────────────────────────
# Subscriber model stores info about each person
# who signs up for the newsletter
# ────────────────────────────────────────────────
class Subscriber(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    company_name = models.CharField(max_length=100, blank=True)  # optional
    email = models.EmailField(unique=True)  # ensures no duplicate emails
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=10)
    signup_date = models.DateTimeField(auto_now_add=True)  # automatically sets current date/time on creation

    def __str__(self):
        # Display full name in the admin panel and dropdowns
        return f"{self.first_name} {self.last_name}"


# ────────────────────────────────────────────────
# Newsletter model stores each newsletter entry
# created by the admin
# ────────────────────────────────────────────────
class Newsletter(models.Model):
    title = models.CharField(max_length=200)
    summary = models.TextField(help_text="Short preview for the email")
    link = models.URLField(help_text="URL of the full newsletter")
    created_at = models.DateTimeField(auto_now_add=True)  # sets when it's created
    is_sent = models.BooleanField(default=False)  # tracks whether it's been sent

    def __str__(self):
        return self.title