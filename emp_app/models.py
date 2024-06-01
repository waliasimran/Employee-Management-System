from django.db import models

# Create your models here.


# the use of ForeignKey for Department and Role fields establishes a
#  relationship between the Employee model and the Department as well as Role
#  models.



# why separate models for department and Role?
#     1) Separating departments and roles into their own models ensures data integrity and consistency.
# 2) You can enforce constraints, validations, and business rules specific to departments and roles separately, ensuring that each entity maintains its integrity.

class Department(models.Model):
    name = models.CharField(max_length=100, null=False)
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Role(models.Model):
    name = models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.name


class Employee(models.Model):
    first_name = models .CharField(max_length=100, null=False)
    last_name = models.CharField(max_length=100)
    dept = models.ForeignKey(Department, on_delete=models.CASCADE)
    salary = models.IntegerField(default=0)
    bonus = models.IntegerField(default=0)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    phone = models.IntegerField(default=0)
    hire_date = models.DateField()

    # The on_delete=models.CASCADE argument specifies that if a referenced department or role is deleted, all associated employees will also be deleted.

    def __str__(self):
        return "%s %s %s %s" % (
            self.first_name, self.last_name, self.phone, self.dept)

# __str__ method is defined to return a formatted string containing the first name, last name, phone number, and department name of the employee when the object is printed.
    
#     ForeignKey is used to establish a relationship between two models in Django, where one model (the "child" or "dependent" model) references another model (the "parent" or "referenced" model).
# in my code what is the parent model and what is the child model

# Employee model is the child model because it contains ForeignKey fields.
# Department and Role models are the parent models because they are being referenced by the Employee model.