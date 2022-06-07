from django.forms import ModelForm, Textarea
from .models import User, Chirp

class ChirpForm(ModelForm):
    class Meta:
        model = Chirp
        fields = ['chirp']
        widgets = {
            'chirp': Textarea(attrs={'cols': 55, 'rows': 5, 'placeholder': 'Post a new chirp!'}),
        }
        labels = {
            'chirp': ''
        }