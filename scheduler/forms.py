# scheduler/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from .models import Event

class CustomUserCreationForm(UserCreationForm):
    # We define our custom fields here
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
        # THIS IS THE CORRECTED LINE
        # We only specify the fields we want to ADD to the form (email)
        fields = UserCreationForm.Meta.fields + ('email',)

# ... The rest of the file (EventForm) remains the same ...
class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'event_time']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter event title'}),
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Enter description'}),
            'event_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }