from django import forms
from django.contrib.auth.models import User

# We are naming it StudentForm to match your import error
class StudentAdmissionForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
           'fields' : ['first_name', 'last_name', 'department', 'current_semester', 'mobile_number', 'date_of_birth', 'tenth_marks', 'twelfth_marks']
        }

StudentForm = StudentAdmissionForm