from mongoengine import Document, StringField, EmailField, IntField, DateTimeField, ReferenceField, DecimalField

class Department(Document):
    name = StringField(max_length=100, required=True)
    description = StringField()

    meta = {
        'collection': 'department'
    }

    def __str__(self):
        return self.name

class Employee(Document):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    ]

    COURSE_CHOICES = [
        ('CSE', 'Computer Science'),
        ('IT', 'Information Technology'),
        ('ECE', 'Electronics & Communication')
    ]

    unique_id = IntField(required=True)
    name = StringField(max_length=100, required=True)
    email = EmailField(unique=True, required=True)
    mobile = StringField(max_length=15, required=True)
    designation = StringField(max_length=100, required=True)
    gender = StringField(max_length=10, required=True)
    courses = StringField(max_length=200, required=True)
    image = StringField(max_length=500, required=False)
    department = ReferenceField('Department', required=False)
    salary = DecimalField(precision=2, required=True)
    hire_date = DateTimeField(required=True)
    address = StringField(required=True)

    meta = {
        'collection': 'employee',
        'indexes': [
            {'fields': ['unique_id'], 'unique': True}
        ]
    }

    def __str__(self):
        return self.name

    def get_gender_display(self):
        return dict(self.GENDER_CHOICES).get(self.gender, '')

    def get_courses_display(self):
        return dict(self.COURSE_CHOICES).get(self.courses, '')

    def save(self, *args, **kwargs):
        if not self.unique_id:
            last_employee = Employee.objects.order_by('-unique_id').first()
            self.unique_id = last_employee.unique_id + 1 if last_employee else 1
        super().save(*args, **kwargs)

