from django import forms
from django.utils.safestring import mark_safe

from .models import Subscriber, Newsletter


# ────────────────────────────────────────────────────────
# Form for users to sign up for the newsletter
# Includes custom checkbox for terms & conditions
# ────────────────────────────────────────────────────────
class SubscriberForm(forms.ModelForm):
    agree_to_terms = forms.BooleanField(
        label=mark_safe(
            'I agree to receive e-mails from your company and accept the '
            '<a href="/terms" target="_blank" class="terms-link">terms and conditions</a>'
        ),
        required=True
    )

    class Meta:
        model = Subscriber
        fields = [
            'first_name',
            'last_name',
            'company_name',
            'email',
            'address',
            'city',
            'state',
            'zipcode',
            'agree_to_terms',
        ]


# ────────────────────────────────────────────────────────
# Form for admin to create or edit a newsletter
# Includes custom placeholders and styles
# ────────────────────────────────────────────────────────
class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = ['title', 'summary', 'link']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'input-box input-short',
                'placeholder': 'Enter a title'
            }),
            'summary': forms.Textarea(attrs={
                'class': 'textarea-box',
                'placeholder': 'Write a short preview…'
            }),
            'link': forms.URLInput(attrs={
                'class': 'input-box input-short',
                'placeholder': 'https://example.com/full-newsletter'
            }),
        }
        labels = {
            'summary': 'Summary',
            'link':    'Link',
        }