# students/forms.py
from django import forms
from dashboard.models import StudentProfile

class StudentAdmissionForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        # Jo fields hume form mein chahiye
        fields = ['first_name', 'last_name', 'roll_no', 'date_of_birth', 'mobile', 'email', 'department']
        
        # Sundar dikhne ke liye Bootstrap classes
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'roll_no': forms.TextInput(attrs={'class': 'form-control'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
        }