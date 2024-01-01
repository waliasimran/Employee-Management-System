from django.shortcuts import render,HttpResponse,get_object_or_404

from .models import Employee,Role,Department
from datetime import datetime
from django.db.models import Q

# Create your views here.

def index(request):
    return render(request,'index.html')

def all_emp_sort(request):
     emps=Employee.objects.all()

    # sort_by = request.GET.get('sort_by')
     
     emps = emps.order_by('salary')
     
     context={
        'emps':emps

    }
    #  print(context)
     return render(request,'view_all_emp.html',context)




def all_emp(request):
    emps=Employee.objects.all()
    print(emps)

    # sort_by = request.GET.get('sort_by')
    context={
        'emps':emps

    }
    # print(context)
    return render(request,'view_all_emp.html',context)



# def add_emp(request):
#     from django.shortcuts import get_object_or_404
# from .models import Employee, Department, Role
# from datetime import datetime
# from django.http import HttpResponse
# from django.shortcuts import render

# def add_emp(request):
#     from django.shortcuts import render, HttpResponse, get_object_or_404
# from .models import Employee, Department, Role
# from datetime import datetime

def add_emp(request):
    # This part of the code executes when the user submits the form via a POST request.
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        salary = int(request.POST['salary'])
        bonus = int(request.POST['bonus'])
        phone = int(request.POST['phone'])
        department_name = request.POST['department']  # Get department name from the form
        role_name = request.POST['role']  # Get role name from the form
        
        # print(request.POST['department'])
        # Retrieve the Department and Role objects based on the provided names
        try:
            department = Department.objects.get(name=department_name)
            role = Role.objects.get(name=role_name)
        except Department.DoesNotExist:
            return HttpResponse('Department not found')
        except Role.DoesNotExist:
            return HttpResponse('Role not found')

        # Create and save the Employee object
        new_emp = Employee(first_name=first_name, last_name=last_name, salary=salary, bonus=bonus, phone=phone, dept=department, role=role, hire_date=datetime.now())
        new_emp.save()
        
        return render(request,'success_add.html')
    

    

    # When the request method is GET, it fetches data or resources
    elif request.method == 'GET':
        departments = Department.objects.all()  # Retrieve all departments
        roles = Role.objects.all()  # Retrieve all roles
        
        context = {
            'departments': departments,
            'roles': roles,
        }
        return render(request, 'add_emp.html', context)
    
    else:
        return HttpResponse("An Exception Occurred! Employee Has Not Been Added")
    



def update_emp(request):
    departments = Department.objects.all()
    if request.method=='POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        new_salary = int(request.POST['salary'])
        department_name = request.POST['department']
        try:
            department = Department.objects.get(name=department_name)
            employee = Employee.objects.get(dept=department, first_name=first_name,last_name=last_name)    
        except Department.DoesNotExist:
            return HttpResponse('Department not found')
        except Employee.DoesNotExist:
            return HttpResponse('Employee not found')
        
        employee.salary = new_salary
        employee.save()

        return render(request,'success_update.html')
    context={
           'departments':departments
    }

    return render(request, 'update_employee.html',context)




def remove_emp(request,emp_id=0):

 if emp_id:
       try:
            emp_to_be_removed=Employee.objects.get(id=emp_id)
            emp_to_be_removed.delete()
            return render(request,'success_remove.html')
       except:
          return HttpResponse("Please enter a valid Employee id")
          
 emps=Employee.objects.all()
 context={
        'emps':emps
       }
 return render(request,'remove_emp.html',context)




def filter_emp(request):
    departments = Department.objects.all()
    roles = Role.objects.all()

    # Q object is used for OR or AND condition in query set
    
    if request.method == 'POST':
        name = request.POST['name']
        dept = request.POST['department']
        depts=Department.objects.get(name=dept)
        role = request.POST['role']
        emps = Employee.objects.all()
        
        if name:
            emps = emps.filter(Q(first_name__icontains = name) | Q(last_name__icontains = name))
        if dept:
            emps = emps.filter(dept__name__icontains = depts)
        if role:
            emps = emps.filter(role__name__icontains = role)

        context = {
            'emps': emps,
            'departments':departments,
            'roles':roles
        }
        return render(request, 'view_all_emp.html', context)

    elif request.method == 'GET':
        context = {
            'departments': departments,
            'roles':roles
        }
        return render(request, 'filter_emp.html',context)
    else:
        return HttpResponse('An Exception Occurred')
    
    