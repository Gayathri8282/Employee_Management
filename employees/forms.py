from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Employee, Department
import datetime
from django.core.validators import validate_email, RegexValidator
from django.core.exceptions import ValidationError

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'email', 'mobile', 'designation', 'gender', 
                 'courses', 'image', 'department', 'salary', 
                 'hire_date', 'address']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'position': forms.TextInput(attrs={'class': 'form-control'}),
            'salary': forms.NumberInput(attrs={'class': 'form-control'}),
            'hire_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
            'placeholder': 'Enter department name',
            'autocomplete': 'off'
        })

class EmployeeRegistrationForm(forms.ModelForm):
    COURSE_CHOICES = [
        ('MCA', 'MCA'),
        ('BCA', 'BCA'),
        ('BSC', 'BSC')
    ]

    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        required=True,
        validators=[validate_email]
    )
    mobile = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'maxlength': '10',
            'minlength': '10',
            'pattern': '[0-9]{10}',
            'title': 'Please enter exactly 10 digits'
        }),
        validators=[
            RegexValidator(
                regex=r'^\d{10}$',
                message='Mobile number must be exactly 10 digits',
                code='invalid_mobile'
            )
        ]
    )
    designation = forms.ChoiceField(
        choices=[('HR', 'HR'), ('Manager', 'Manager'), ('Sales', 'Sales')],
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )
    gender = forms.ChoiceField(
        choices=[('M', 'Male'), ('F', 'Female')],
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        required=True
    )
    courses = forms.ChoiceField(
        choices=COURSE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )
    image = forms.ImageField(
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/jpeg,image/png'}),
        required=False
    )
    department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )
    salary = forms.DecimalField(
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        required=True
    )
    hire_date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        initial=datetime.date.today,
        required=True
    )
    address = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        required=True
    )

    class Meta:
        model = Employee
        fields = ['name', 'email', 'mobile', 'designation', 'gender', 
                 'courses', 'image', 'department', 'salary', 
                 'hire_date', 'address']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Employee.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already registered.')
        return email

    def clean_mobile(self):
        mobile = self.cleaned_data.get('mobile')
        if not mobile.isdigit():
            raise forms.ValidationError('Please enter only digits')
        if len(mobile) != 10:
            raise forms.ValidationError('Mobile number must be exactly 10 digits')
        return mobile

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            if not image.name.lower().endswith(('.jpg', '.jpeg', '.png')):
                raise forms.ValidationError('Only JPG/PNG files are allowed.')
        return image