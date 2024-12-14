from django.core.management.base import BaseCommand
from employees.models import Employee as OldEmployee, Department as OldDepartment
from employees.models import Employee, Department

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        # Migrate Departments first
        for old_dept in OldDepartment.objects.all():
            new_dept = Department(
                name=old_dept.name,
                description=old_dept.description,
                created_at=old_dept.created_at
            )
            new_dept.save()

        # Then migrate Employees
        for old_emp in OldEmployee.objects.all():
            new_dept = Department.objects(name=old_emp.department.name).first()
            new_emp = Employee(
                name=old_emp.name,
                email=old_emp.email,
                mobile=old_emp.mobile,
                designation=old_emp.designation,
                gender=old_emp.gender,
                courses=old_emp.courses,
                hire_date=old_emp.hire_date,
                department=new_dept,
                salary=old_emp.salary,
                address=old_emp.address
            )
            if old_emp.image:
                new_emp.image.put(old_emp.image.read())
            new_emp.save()