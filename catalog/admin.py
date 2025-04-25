from django.contrib import admin
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

from .models import Subscriber, Newsletter

@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'signup_date')
    search_fields = ('first_name', 'last_name', 'email')

@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'is_sent')
    actions = ['send_newsletter']

    def send_newsletter(self, request, queryset):
        for newsletter in queryset:
            if newsletter.is_sent:
                continue  # skip already‐sent

            subscribers = Subscriber.objects.all()
            for subscriber in subscribers:
                # Render the HTML email template
                html_content = render_to_string(
                    'newsletter_email.html',
                    {'newsletter': newsletter, 'subscriber': subscriber}
                )
                # Create plain‐text version
                text_content = strip_tags(html_content)

                # Build the email
                email = EmailMultiAlternatives(
                    subject=newsletter.title,
                    body=text_content,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[subscriber.email],
                )
                email.attach_alternative(html_content, "text/html")
                email.send()

            # Mark this newsletter as sent
            newsletter.is_sent = True
            newsletter.save()

        self.message_user(request, "Newsletter(s) sent successfully.")
    send_newsletter.short_description = "Send selected newsletters"