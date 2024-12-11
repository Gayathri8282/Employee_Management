from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from .models import Employee, Department
from .forms import EmployeeForm, DepartmentForm
from django.db.models import Avg

@login_required
def dashboard(request):
    total_employees = Employee.objects.filter(is_active=True).count()
    avg_salary = Employee.objects.filter(is_active=True).aggregate(Avg('salary'))['salary__avg']
    departments = Department.objects.all().count()
    
    context = {
        'total_employees': total_employees,
        'average_salary': avg_salary,
        'departments': departments,
    }
    return render(request, 'dashboard.html', context)

@login_required
def employee_list(request):
    employees = Employee.objects.filter(is_active=True)
    return render(request, 'employees/employee_list.html', {'employees': employees})

@login_required
def employee_detail(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    return render(request, 'employees/employee_detail.html', {'employee': employee})

@login_required
def employee_create(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            employee = form.save()
            messages.success(request, 'Employee created successfully.')
            return redirect('employee_list')
    else:
        form = EmployeeForm()
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
    return render(request, 'employees/employee_form.html', {'form': form})

@login_required
def employee_delete(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        employee.is_active = False
        employee.save()
        messages.success(request, 'Employee deleted successfully.')
        return redirect('employee_list')
    return render(request, 'employees/employee_confirm_delete.html', {'employee': employee})

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully.')
    return redirect('login')

@login_required
def department_list(request):
    departments = Department.objects.all()
    return render(request, 'departments/department_list.html', {'departments': departments})

@login_required
def department_create(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Department created successfully.')
            return redirect('department_list')
    else:
        form = DepartmentForm()
    return render(request, 'departments/department_form.html', {'form': form})