from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Employee, Department
import datetime
from django.core.validators import validate_email, RegexValidator
import uuid
import os
from django.conf import settings
import time

class EmployeeRegistrationForm(forms.Form):
    DESIGNATION_CHOICES = [
        ('', 'Select Designation'),
        ('HR', 'HR'),
        ('Manager', 'Manager'),
        ('Sales', 'Sales')
    ]

    COURSE_CHOICES = [
        ('CSE', 'Computer Science'),
        ('IT', 'Information Technology'),
        ('ECE', 'Electronics & Communication')
    ]

    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}), required=True, validators=[validate_email])
    mobile = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'maxlength': '10', 'minlength': '10', 'pattern': '[0-9]{10}', 'title': 'Please enter exactly 10 digits'}),
        validators=[RegexValidator(regex=r'^\d{10}$', message='Mobile number must be exactly 10 digits', code='invalid_mobile')]
    )
    designation = forms.ChoiceField(
        choices=DESIGNATION_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control mb-2'
        }),
        required=True
    )
    
    custom_designation = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control mt-2',
            'placeholder': 'Or type your own designation'
        })
    )

    # Multiple choice field for predefined courses
    predefined_courses = forms.MultipleChoiceField(
        choices=COURSE_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-check-input mr-2'
        })
    )

    # Text field for custom course
    custom_courses = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control mt-2',
            'placeholder': 'Or type your own course'
        })
    )

    gender = forms.ChoiceField(choices=[('M', 'Male'), ('F', 'Female')], widget=forms.RadioSelect(attrs={'class': 'form-check-input'}), required=True)
    image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/jpeg,image/png'}), required=False)
    
    # Custom field for department selection
    department = forms.ChoiceField(
        choices=[(dept.id, dept.name) for dept in Department.objects.all()],
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )
    
    salary = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control'}), required=True)
    hire_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}), initial=datetime.date.today, required=True)
    address = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}), required=True)

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop('instance', None)  # Add this line
        super().__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if self.instance:
            # Exclude current instance when checking for duplicate email
            existing = Employee.objects.filter(email=email).first()
            if existing and existing.unique_id != self.instance.unique_id:
                raise forms.ValidationError('This email is already registered.')
        else:
            # Check for duplicate email only when creating new employee
            if Employee.objects.filter(email=email).first():
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

    def clean(self):
        cleaned_data = super().clean()
        # Get the designation value
        if cleaned_data.get('custom_designation'):
            cleaned_data['designation'] = cleaned_data['custom_designation']
        
        # Handle courses
        courses = []
        if cleaned_data.get('predefined_courses'):
            courses.extend(cleaned_data['predefined_courses'])
        if cleaned_data.get('custom_courses'):
            courses.append(cleaned_data['custom_courses'])
        
        # If no courses selected, use default
        if not courses:
            courses = ['Not Specified']
        
        cleaned_data['courses'] = ', '.join(courses)
        return cleaned_data

    def save(self):
        if self.instance:
            # Update existing employee
            self.instance.name = self.cleaned_data['name']
            self.instance.email = self.cleaned_data['email']
            self.instance.mobile = self.cleaned_data['mobile']
            self.instance.designation = self.cleaned_data['designation']
            self.instance.gender = self.cleaned_data['gender']
            
            # Handle courses - convert list to string if necessary
            courses = self.cleaned_data['courses']
            if isinstance(courses, (list, tuple)):
                courses = ', '.join(courses)
            self.instance.courses = courses
            
            self.instance.salary = self.cleaned_data['salary']
            self.instance.hire_date = self.cleaned_data['hire_date']
            self.instance.address = self.cleaned_data['address']
            
            # Handle image upload
            if 'image' in self.cleaned_data and self.cleaned_data['image']:
                if hasattr(self.cleaned_data['image'], 'name'):
                    # Generate unique filename
                    ext = os.path.splitext(self.cleaned_data['image'].name)[1]
                    filename = f'employee_{self.instance.unique_id}_{int(time.time())}{ext}'
                    filepath = os.path.join('employee_images', filename)
                    
                    # Save file to media directory
                    with open(os.path.join(settings.MEDIA_ROOT, filepath), 'wb+') as destination:
                        for chunk in self.cleaned_data['image'].chunks():
                            destination.write(chunk)
                    
                    self.instance.image = filepath
            
            self.instance.save()
            return self.instance
        else:
            # Create new employee
            employee = Employee(
                name=self.cleaned_data['name'],
                email=self.cleaned_data['email'],
                mobile=self.cleaned_data['mobile'],
                designation=self.cleaned_data['designation'],
                gender=self.cleaned_data['gender'],
                courses=self.cleaned_data['courses'] if isinstance(self.cleaned_data['courses'], str) 
                        else ', '.join(self.cleaned_data['courses']),
                salary=self.cleaned_data['salary'],
                hire_date=self.cleaned_data['hire_date'],
                address=self.cleaned_data['address']
            )
            
            # Handle image for new employee
            if 'image' in self.cleaned_data and self.cleaned_data['image']:
                if hasattr(self.cleaned_data['image'], 'name'):
                    ext = os.path.splitext(self.cleaned_data['image'].name)[1]
                    filename = f'employee_new_{int(time.time())}{ext}'
                    filepath = os.path.join('employee_images', filename)
                    
                    with open(os.path.join(settings.MEDIA_ROOT, filepath), 'wb+') as destination:
                        for chunk in self.cleaned_data['image'].chunks():
                            destination.write(chunk)
                    
                    employee.image = filepath
            
            employee.save()
            return employee

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class DepartmentForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}), required=False)

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop('instance', None)  # Get instance if it exists
        super().__init__(*args, **kwargs)
        
        # Set initial values if editing an existing department
        if self.instance:
            self.fields['name'].initial = self.instance.name
            self.fields['description'].initial = self.instance.description

        self.fields['name'].widget.attrs.update({
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
            'placeholder': 'Enter department name',
            'autocomplete': 'off'
        })

    def save(self):
        if self.instance:
            # Update existing department
            self.instance.name = self.cleaned_data['name']
            self.instance.description = self.cleaned_data.get('description', '')
            self.instance.save()
            return self.instance
        else:
            # Create new department
            department = Department(
                name=self.cleaned_data['name'],
                description=self.cleaned_data.get('description', '')
            )
            department.save()
            return department