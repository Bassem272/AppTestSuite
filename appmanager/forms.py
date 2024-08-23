# accounts/forms.py
from django import forms
from .models import App

class AppForm(forms.ModelForm):
    class Meta:
        model = App
        fields = ['name', 'apk_file']

