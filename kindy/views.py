from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from childcare.models import Childcare


@login_required
def home(request):
    childcare_list = Childcare.objects.filter(managers__id=request.user.pk)
    return render(request, 'kindy/home.html', {'childcare_list': childcare_list})