from django import forms
from .models import StaffProfile

class StaffForm(forms.ModelForm):
    class Meta:
        model = StaffProfile
        fields = '__all__'