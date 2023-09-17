from django import forms
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
import re



class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label=_("Email"),
        help_text=_("Please enter a valid email address.")
    )
    unit = forms.ChoiceField(
        choices=UserProfile.UNIT_CHOICES,
        widget=forms.RadioSelect,
        initial='ml',
        label=_("Unit"),
        help_text=_("Please select your preferred unit.")
    )
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2", "unit"]

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            clean_help_text = field.help_text
            if isinstance(clean_help_text, str):  # Check if it's a string
                clean_help_text = re.sub(r'<.*?>', '', clean_help_text)
            field.widget.attrs['title'] = clean_help_text
            field.widget.attrs['data-bs-toggle'] = 'tooltip'
            field.help_text = ''
