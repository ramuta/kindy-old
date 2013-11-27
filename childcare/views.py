from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from guardian.decorators import permission_required_or_403
from childcare.forms import ChildcareCreateForm
from childcare.models import Childcare
from classroom.models import Classroom


@login_required
def childcare_create(request):
    if request.method == 'POST':
        form = ChildcareCreateForm(request.POST)
        if form.is_valid():
            managers = form.cleaned_data['managers']
            childcare = form.save(commit=True)
            # add manager permissions
            group = Group.objects.get(name='Childcare %s: Manager' % childcare.pk)
            for manager in managers:
                manager.groups.add(group)
            # add default classroom
            classroom = Classroom(name='%s classroom' % childcare, childcare=childcare)
            classroom.save()
            return HttpResponseRedirect('/%s/dashboard/' % childcare.slug)
    else:
        form = ChildcareCreateForm()
    return render(request, 'childcare/childcare_create.html', {'form': form})


@login_required
@permission_required_or_403('childcare_view', (Childcare, 'slug', 'childcare_slug'))
def childcare(request, childcare_slug):
    childcare = get_object_or_404(Childcare, slug=childcare_slug)
    classroom_list = Classroom.objects.filter(childcare=childcare)
    manager_list = User.objects.filter(childcare_managers__id=childcare.pk)
    return render(request, 'childcare/childcare_detail.html', {'childcare': childcare,
                                                               'classroom_list': classroom_list,
                                                               'manager_list': manager_list})