from django import forms
from .models import Employee, Department
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class EmployeeForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()

    class Meta:
        model = Employee
        fields = ['department', 'position', 'salary', 'hire_date', 'phone', 'address']

    def save(self, commit=True):
        employee = super().save(commit=False)
        if commit:
            employee.save()
        return employee

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'description'] 