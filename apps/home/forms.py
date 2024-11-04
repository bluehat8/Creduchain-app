# apps/home/forms.py
from django import forms
from .models import Student

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'student_name', 
            'student_last_name', 
            'student_id', 
            'city', 
            'program', 
            'horary_zone', 
            'graduation_date'
        ]
        widgets = {
            'student_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            'student_last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido'}),
            'student_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ID del estudiante'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ciudad'}),
            'program': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Programa'}),
            'horary_zone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Zona horaria'}),
            'graduation_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
