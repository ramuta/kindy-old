from django.contrib.auth.models import Group
from guardian.shortcuts import assign_perm
import childcare


def roles_childcare_init_new(childcare_obj):
    # new role groups for childcare
    childcare_employees = Group.objects.get_or_create(name='Childcare %s: Employee' % childcare_obj.pk)[0]
    childcare_managers = Group.objects.get_or_create(name='Childcare %s: Manager' % childcare_obj.pk)[0]
    childcare_parents = Group.objects.get_or_create(name='Childcare %s: Parent' % childcare_obj.pk)[0]

    assign_perm('childcare_view', childcare_managers, childcare_obj)
    assign_perm('childcare_employee', childcare_managers, childcare_obj)
    assign_perm('childcare_admin', childcare_managers, childcare_obj)

    assign_perm('childcare_view', childcare_employees, childcare_obj)
    assign_perm('childcare_employee', childcare_employees, childcare_obj)

    assign_perm('childcare_view', childcare_parents, childcare_obj)

    childcare.models.GroupChildcare.objects.get_or_create(group=childcare_employees, childcare=childcare_obj)
    childcare.models.GroupChildcare.objects.get_or_create(group=childcare_managers, childcare=childcare_obj)
    childcare.models.GroupChildcare.objects.get_or_create(group=childcare_parents, childcare=childcare_obj)
    return True