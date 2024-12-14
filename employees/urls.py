from django.urls import path
from . import views
from bson import ObjectId  # Import ObjectId if needed

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('employee/list/', views.employee_list, name='employee_list'),
    path('employee/create/', views.employee_create, name='employee_create'),
    path('employee/<int:unique_id>/edit/', views.employee_edit, name='employee_edit'),
    path('employee/<int:unique_id>/delete/', views.employee_delete, name='employee_delete'),
    
    # Department URLs
    path('department/list/', views.department_list, name='department_list'),
    path('departments/create/', views.department_create, name='department_create'),
    path('departments/<str:id>/edit/', views.department_edit, name='department_edit'),
    path('departments/<str:id>/delete/', views.department_delete, name='department_delete'),
    
    # AJAX endpoints
    path('check-email/', views.check_email, name='check_email'),
    
    # Authentication URLs (if you want custom login/logout views)
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
] 