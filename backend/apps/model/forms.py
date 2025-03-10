from django import forms
from apps.model.models import Model
from django.core.files.uploadedfile import InMemoryUploadedFile

# Create the form class.
class CreateForm(forms.ModelForm):
    class Meta:
        model = Model
        fields = ['modelo', 'tipo', 'k']
        widgets = {
            'k': forms.NumberInput(attrs={'placeholder': '20'}),
        }
