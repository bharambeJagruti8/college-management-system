from django import forms
from .models import Student, Staff


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'

class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ['name', 'email', 'department']