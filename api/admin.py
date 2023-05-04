from django.contrib import admin

# Register your models here.
from .models import Department, Employee

admin.site.register(Department)
admin.site.register(Employee)