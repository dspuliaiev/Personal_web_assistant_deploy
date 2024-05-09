from django import forms
from django.core.validators import RegexValidator
from .models import Contact

phone_regex = RegexValidator(
    regex=r'^\+?[1-9]\d{1,14}$',
    message="Phone number must be entered in the format: '+<country_code><number>'. Up to 15 digits allowed."
)

class ContactForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}))
    phone_number = forms.CharField(
        max_length=15,
        validators=[phone_regex],
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    birthday = forms.DateField(widget=forms.DateInput(attrs={"class": "form-control"}))

    class Meta:
        model = Contact
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'birthday']
        error_messages = {
            'email': {
                'invalid': "Please enter a valid email address.",
            },
        }

    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        email = cleaned_data.get('email')
        phone_number = cleaned_data.get('phone_number')
        birthday = cleaned_data.get('birthday')

        if not first_name:
            self.add_error('first_name', 'This field is required.')
        if not last_name:
            self.add_error('last_name', 'This field is required.')
        if not email:
            self.add_error('email', 'This field is required.')
        if not phone_number:
            self.add_error('phone_number', 'This field is required.')
        if not birthday:
            self.add_error('birthday', 'This field is required.')

        return cleaned_data

        
