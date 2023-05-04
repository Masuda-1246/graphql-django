from django.db import models

# Create your models here.

class Department(models.Model):
    department_name = models.CharField(max_length=100)

    def __str__(self):
        return self.department_name

class Employee(models.Model):
    employee_name = models.CharField(max_length=100)
    join_year = models.IntegerField()
    department = models.ForeignKey(Department,related_name='employees', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.employee_name