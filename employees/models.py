from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator, MaxLengthValidator, RegexValidator

class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Employee(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female')
    ]
    
    DESIGNATION_CHOICES = [
        ('HR', 'HR'),
        ('Manager', 'Manager'),
        ('Sales', 'Sales')
    ]

    COURSE_CHOICES = [
        ('MCA', 'MCA'),
        ('BCA', 'BCA'),
        ('BSC', 'BSC')
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    mobile = models.CharField(
        max_length=10,
        validators=[
            MinLengthValidator(10),
            MaxLengthValidator(10),
            RegexValidator(
                regex=r'^\d{10}$',
                message='Mobile number must be exactly 10 digits',
                code='invalid_mobile'
            )
        ]
    )
    designation = models.CharField(max_length=20, choices=DESIGNATION_CHOICES)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    courses = models.CharField(max_length=3, choices=COURSE_CHOICES)
    image = models.ImageField(upload_to='employee_images/', null=True, blank=True)
    hire_date = models.DateField()
    department = models.ForeignKey('Department', on_delete=models.CASCADE)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    address = models.TextField()

    def __str__(self):
        return self.name

