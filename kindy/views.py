from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from childcare.models import Childcare


@login_required
def home(request):
    childcare_list_manager = Childcare.objects.filter(managers__id=request.user.pk)
    childcare_list_employee = Childcare.objects.filter(employees__id=request.user.pk)
    childcare_list_parent = Childcare.objects.filter(parents__id=request.user.pk)
    return render(request, 'kindy/home.html', {'childcare_list_manager': childcare_list_manager,
                                               'childcare_list_employee': childcare_list_employee,
                                               'childcare_list_parent': childcare_list_parent})