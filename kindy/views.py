from itertools import chain
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from childcare.models import Childcare


@login_required
def home(request):
    childcare_list_manager = Childcare.objects.filter(managers__id=request.user.pk)
    childcare_list_employee = Childcare.objects.filter(employees__id=request.user.pk)
    childcare_list_parent = Childcare.objects.filter(parents__id=request.user.pk)

    all_childcare_list = list(set(chain(childcare_list_manager, childcare_list_employee, childcare_list_parent)))  # set for removing duplicates, chain for chaining lists
    return render(request, 'kindy/home.html', {'all_childcare_list': all_childcare_list})