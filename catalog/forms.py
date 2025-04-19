from django import forms
from .models import Subscriber
from django.utils.safestring import mark_safe

class SubscriberForm(forms.ModelForm):
    agree_to_terms = forms.BooleanField(
        label=mark_safe(
            'I agree to receive e‑mails from your company and accept the '
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