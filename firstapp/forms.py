from django import forms
from django.forms import DateTimeInput
from .models import Event
from .models import Payment
class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['college_name', 'event_name', 'address', 'college_website', 'event_datetime', 'event_brochure', 'coordinator_name', 'coordinator_contact', 'event_description','entry_fee']
        
        widgets = {
            'event_datetime': DateTimeInput(attrs={'type': 'datetime-local'}),
        }
        input_formats = {
            'event_datetime': ['%Y-%m-%dT%H:%M', '%Y-%m-%d %H:%M', '%Y-%m-%d %H:%M:%S'],
        }

from .models import Payment

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['email', 'eventname', 'amount']
