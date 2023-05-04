import graphene
from graphene_django import DjangoObjectType
from .models import Department, Employee
from graphene_django.filter import DjangoFilterConnectionField
from graphene import relay
from graphql_relay import from_global_id
from graphql_jwt_decorators import login_required


class EmployeeNode(DjangoObjectType):
    class Meta:
        model = Employee
        filter_fields = {
          'employee_name': ['exact', 'icontains'],
          'join_year': ['exact', 'icontains'],
          'department': ['icontains'],
        }
        interfaces = (relay.Node, )

class DepartmentNode(DjangoObjectType):
    class Meta:
        model = Department
        filter_fields = {
          'department_name': ['exact'],
          'employees': ['exact'],
        }
        interfaces = (relay.Node, )

class Query(graphene.ObjectType):
    employee = graphene.Field(EmployeeNode, id=graphene.NonNull(graphene.ID))
    all_employees = DjangoFilterConnectionField(EmployeeNode)
    all_departments = DjangoFilterConnectionField(DepartmentNode)

    @login_required
    def resolve_employee(self, info, **kwargs):
      id = kwargs.get('id')
      if id is not None:
        return Employee.objects.get(id=from_global_id(id)[1])

    @login_required
    def resolve_all_employees(self, info, **kwargs):
      return Employee.objects.all()

    @login_required
    def resolve_all_departments(self, info, **kwargs):
      return Department.objects.all()
