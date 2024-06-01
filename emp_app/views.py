
from django.shortcuts import render, HttpResponse
from .models import Employee, Role, Department
from datetime import datetime
from django.db.models import Q

# The Q object allows you to construct complex queries by combining multiple conditions using logical operators.

# Create your views here.


def index(request):
    return render(request, 'index.html')


def all_emp_sort(request):
    emps = Employee.objects.all()
    emps = emps.order_by('salary')
    context = {
        'emps': emps
    }
    return render(request, 'view_all_emp.html', context)


def all_emp(request):
    emps = Employee.objects.all()
    print(emps)
    context = {
        'emps': emps
    }
    return render(request, 'view_all_emp.html', context)


def add_emp(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        salary = int(request.POST['salary'])
        bonus = int(request.POST['bonus'])
        phone = int(request.POST['phone'])
        department_name = request.POST['department']
        role_name = request.POST['role']

        try:
            department = Department.objects.get(name=department_name)
            role = Role.objects.get(name=role_name)
        except Department.DoesNotExist:
            return HttpResponse('Department not found')
        except Role.DoesNotExist:
            return HttpResponse('Role not found')

        new_emp = Employee(first_name=first_name, last_name=last_name,
                           salary=salary,
                           bonus=bonus, phone=phone, dept=department,
                           role=role, hire_date=datetime.now())
        new_emp.save()

        return render(request, 'success_add.html')

    elif request.method == 'GET':
        departments = Department.objects.all()
        roles = Role.objects.all()

        context = {
            'departments': departments,
            'roles': roles,
        }
        return render(request, 'add_emp.html', context)
    else:
        return HttpResponse
    ("An Exception Occurred! Employee Has Not Been Added")


# POST Method: In the provided code, the POST method is used to handle form submissions for adding a new employee. It retrieves form data from the request body and saves it to the server, modifying server-side data (i.e., adding a new employee).
# GET Method: The GET method, on the other hand, is used to initially display the form for adding a new employee. It retrieves existing data (departments and roles) from the server and renders an HTML form for user input without modifying any server-side data.
# In essence, POST is used for sending data to the server to modify it, while GET is used for retrieving data from the server without modifying it.






def update_emp(request):
    departments = Department.objects.all()
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        new_salary = int(request.POST['salary'])
        department_name = request.POST['department']
        try:
            department = Department.objects.get(name=department_name)
            employee = Employee.objects.get(dept=department,
                                            first_name=first_name,
                                            last_name=last_name)
        except Department.DoesNotExist:
            return HttpResponse('Department not found')
        except Employee.DoesNotExist:
            return HttpResponse('Employee not found')
        employee.salary = new_salary
        employee.save()

        return render(request, 'success_update.html')
    context = {
        'departments': departments
    }
    return render(request, 'update_employee.html', context)


def remove_emp(request, emp_id=0):
    if emp_id:
        try:
            emp_to_be_removed = Employee.objects.get(id=emp_id)
            emp_to_be_removed.delete()
            return render(request, 'success_remove.html')
        except Employee.DoesNotExist:
            return HttpResponse("Employee with the provided ID does not exist")
        except Exception as e:
            # Catch any other unexpected exceptions and handle them
            return HttpResponse(f"An unexpected error occurred: {str(e)}")
    emps = Employee.objects.all()
    context = {
        'emps': emps
    }
    return render(request, 'remove_emp.html', context)


def filter_emp(request):
    departments = Department.objects.all()
    roles = Role.objects.all()

    if request.method == 'POST':
        name = request.POST['name']
        dept = request.POST['department']
        depts = Department.objects.get(name=dept)
        role = request.POST['role']
        emps = Employee.objects.all()
        if name:
            emps = emps.filter(Q(first_name__icontains=name) | Q
                               (last_name__icontains=name))
        if dept:
            emps = emps.filter(dept__name__icontains=depts)
        if role:
            emps = emps.filter(role__name__icontains=role)

        context = {
            'emps': emps,
            'departments': departments,
            'roles': roles
        }
        return render(request, 'view_all_emp.html', context)

    elif request.method == 'GET':
        context = {
            'departments': departments,
            'roles': roles
        }
        return render(request, 'filter_emp.html', context)
    else:
        return HttpResponse('An Exception Occurred')
