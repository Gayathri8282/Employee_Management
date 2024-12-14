from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Avg, Q
from .models import Employee, Department
from .forms import UserRegistrationForm, DepartmentForm, EmployeeRegistrationForm
from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.http import JsonResponse
from bson import ObjectId
import os
from django.conf import settings

@login_required
def dashboard(request):
    total_employees = Employee.objects.count()
    total_departments = Department.objects.count()
    
    context = {
        'total_employees': total_employees,
        'total_departments': total_departments,
    }
    return render(request, 'employees/dashboard.html', context)

@login_required
def employee_list(request):
    search_query = request.GET.get('search', '')
    employees = Employee.objects.all().order_by('-hire_date')

    if search_query:
        employees = employees.filter(
            Q(name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(mobile__icontains=search_query) |
            Q(designation__icontains=search_query) |
            Q(courses__icontains=search_query)
        )

    context = {
        'employees': employees,
        'search_query': search_query,
    }
    return render(request, 'employees/employee_list.html', context)

@login_required
def employee_detail(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    return render(request, 'employees/employee_detail.html', {'employee': employee})

@login_required
def employee_create(request):
    if request.method == 'POST':
        form = EmployeeRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            employee = form.save()
            messages.success(request, 'Employee created successfully!')
            return redirect('employee_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = EmployeeRegistrationForm()
    return render(request, 'employees/employee_form.html', {'form': form})

@login_required
def employee_update(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            messages.success(request, 'Employee updated successfully.')
            return redirect('employee_detail', pk=pk)
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'employees/employee_form.html', {'form': form, 'employee': employee})

@login_required
def employee_delete(request, unique_id):
    try:
        employee = Employee.objects.get(unique_id=int(unique_id))
        
        # Delete the employee's image file if it exists
        if employee.image:
            image_path = os.path.join(settings.MEDIA_ROOT, str(employee.image))
            if os.path.exists(image_path):
                os.remove(image_path)
        
        # Delete the employee record
        employee.delete()
        
        messages.success(request, 'Employee deleted successfully!')
        return redirect('employee_list')
    
    except Employee.DoesNotExist:
        messages.error(request, 'Employee not found!')
        return redirect('employee_list')
    except Exception as e:
        messages.error(request, f'An error occurred while deleting: {str(e)}')
        return redirect('employee_list')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}. You can now log in.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'employees/register.html', {'form': form})

@login_required
def department_list(request):
    departments = Department.objects.all()
    return render(request, 'employees/department_list.html', {'departments': departments})

@login_required
def department_create(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Department created successfully!')
            return redirect('department_list')
    else:
        form = DepartmentForm()
    return render(request, 'employees/department_form.html', {'form': form})

@login_required
def department_edit(request, pk):
    department = Department.objects.get(id=ObjectId(pk))
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            messages.success(request, f'Department "{department.name}" has been updated successfully!')
            return redirect('department_list')
    else:
        form = DepartmentForm(instance=department)
    
    return render(request, 'employees/department_edit.html', {
        'form': form,
        'department': department
    })

@login_required
def department_delete(request, pk):
    department = get_object_or_404(Department, id=ObjectId(pk))
    if request.method == 'POST':
        department.delete()
        messages.success(request, 'Department deleted successfully!')
        return redirect('department_list')
    return render(request, 'employees/department_confirm_delete.html', {'department': department})

def logout_view(request):
    logout(request)
    return redirect('login')

def employee_view(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    return render(request, 'employees/employee_detail.html', {'employee': employee})

@login_required
def employee_edit(request, unique_id):
    try:
        employee = Employee.objects.get(unique_id=int(unique_id))
        if request.method == 'POST':
            form = EmployeeRegistrationForm(request.POST, request.FILES, instance=employee)
            if form.is_valid():
                form.save()
                messages.success(request, 'Employee updated successfully!')
                return redirect('employee_list')
        else:
            initial_data = {
                'name': employee.name,
                'email': employee.email,
                'mobile': employee.mobile,
                'designation': employee.designation,
                'gender': employee.gender,
                'courses': employee.courses,
                'department': employee.department.id if employee.department else None,
                'salary': employee.salary,
                'hire_date': employee.hire_date,
                'address': employee.address
            }
            form = EmployeeRegistrationForm(initial=initial_data, instance=employee)
        return render(request, 'employees/employee_form.html', {
            'form': form,
            'employee': employee
        })
    except Employee.DoesNotExist:
        messages.error(request, 'Employee not found!')
        return redirect('employee_list')
    except Exception as e:
        messages.error(request, f'An error occurred: {str(e)}')
        return redirect('employee_list')

@login_required
def employee_delete(request, unique_id):
    try:
        employee = Employee.objects.get(unique_id=int(unique_id))
        
        # Delete the employee's image file if it exists
        if employee.image:
            image_path = os.path.join(settings.MEDIA_ROOT, str(employee.image))
            if os.path.exists(image_path):
                os.remove(image_path)
        
        # Delete the employee record
        employee.delete()
        
        messages.success(request, 'Employee deleted successfully!')
        return redirect('employee_list')
    
    except Employee.DoesNotExist:
        messages.error(request, 'Employee not found!')
        return redirect('employee_list')
    except Exception as e:
        messages.error(request, f'An error occurred while deleting: {str(e)}')
        return redirect('employee_list')

def employee_register(request):
    if request.method == 'POST':
        form = EmployeeRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            employee = form.save(commit=False)
            employee.save()
            messages.success(request, 'Employee registered successfully!')
            return redirect('employee_list')
    else:
        form = EmployeeRegistrationForm()
    return render(request, 'employees/employee_register.html', {'form': form})

def check_email(request):
    email = request.GET.get('email', None)
    if email:
        exists = Employee.objects.filter(email=email).first() is not None
        return JsonResponse({'exists': exists})
    return JsonResponse({'exists': False})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'registration/login.html')