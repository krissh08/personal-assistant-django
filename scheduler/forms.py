# scheduler/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from .models import Event

class CustomUserCreationForm(UserCreationForm):
    # Our custom fields are defined here
    email = forms.EmailField(required=True)
    username = forms.CharField(
        max_length=12,
        help_text='Required. 12 characters or fewer. Letters, numbers, and . _ characters only.',
        validators=[
            RegexValidator(
                r'^[a-zA-Z0-9._]+$',
                'Enter a valid username. This value may contain only letters, numbers, and . / _ characters.'
            ),
        ],
    )

    class Meta(UserCreationForm.Meta):
        model = User
        # THIS IS THE KEY: We must list all fields to ensure they are
        # included in the form. This was the source of all the problems.
        fields = ("username", "email", "password", "password2")


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'event_time']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter event title'}),
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Enter description'}),
            'event_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }