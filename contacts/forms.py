from django import forms
from .models import Contact

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'birthday']
        error_messages = {
            'phone_number': {
                'invalid': "Please enter a valid phone number.",
            },
            'email': {
                'invalid': "Please enter a valid email address.",
            },
        }