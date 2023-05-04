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

class DeptCreateMutation(relay.ClientIDMutation):
    class Input:
        department_name = graphene.String(required=True)

    department = graphene.Field(DepartmentNode)

    @login_required
    def mutate_and_get_payload(root, info, **input):
        department = Department(department_name=input.get('department_name'))
        department.save()
        return DeptCreateMutation(department=department)

class DeptDeleteMutation(relay.ClientIDMutation):
    class Input:
        id = graphene.ID(required=True)

    department = graphene.Field(DepartmentNode)

    @login_required
    def mutate_and_get_payload(root, info, **input):
        department = Department(id=from_global_id(input.get('id'))[1])
        department.delete()
        return DeptDeleteMutation(department=None)

class EmployeeCreateMutation(relay.ClientIDMutation):
    class Input:
        employee_name = graphene.String(required=True)
        join_year = graphene.Int(required=True)
        department = graphene.ID(required=True)

    employee = graphene.Field(EmployeeNode)

    @login_required
    def mutate_and_get_payload(root, info, **input):
        employee = Employee(employee_name=input.get('employee_name'), join_year=input.get('join_year'), department_id=from_global_id(input.get('department'))[1])
        employee.save()
        return EmployeeCreateMutation(employee=employee)

class EmployeeUpdateMutation(relay.ClientIDMutation):
    class Input:
        id = graphene.ID(required=True)
        employee_name = graphene.String(required=True)
        join_year = graphene.Int(required=True)
        department = graphene.ID(required=True)
    
    employee = graphene.Field(EmployeeNode)
    
    @login_required
    def mutate_and_get_payload(root, info, **input):
        employee = Employee(id=from_global_id(input.get('id'))[1])
        employee.employee_name = input.get('employee_name')
        employee.join_year = input.get('join_year')
        employee.department_id = from_global_id(input.get('department'))[1]
        employee.save()
        return EmployeeUpdateMutation(employee=employee)

class EmployeeDeleteMutation(relay.ClientIDMutation):
    class Input:
        id = graphene.ID(required=True)

    employee = graphene.Field(EmployeeNode)

    @login_required
    def mutate_and_get_payload(root, info, **input):
        employee = Employee(id=from_global_id(input.get('id'))[1])
        employee.delete()
        return EmployeeDeleteMutation(employee=None)

class Mutation(graphene.AbstractType):
    create_department = DeptCreateMutation.Field()
    delete_department = DeptDeleteMutation.Field()
    create_employee = EmployeeCreateMutation.Field()
    update_employee = EmployeeUpdateMutation.Field()
    delete_employee = EmployeeDeleteMutation.Field()
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
