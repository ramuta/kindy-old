from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from guardian.decorators import permission_required_or_403
from childcare.models import Childcare
from classroom.forms import ClassroomCreateForm, DiaryCreateForm
from classroom.models import Classroom, Diary
from django.db import IntegrityError


@login_required
@permission_required_or_403('childcare_employee', (Childcare, 'slug', 'childcare_slug'))
def classroom_create(request, childcare_slug):
    childcare = get_object_or_404(Childcare, slug=childcare_slug)
    if request.method == 'POST':
        form = ClassroomCreateForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.childcare = childcare
            obj.save()
            form.save(commit=True)
            return HttpResponseRedirect('/%s/dashboard/' % childcare_slug)
    else:
        form = ClassroomCreateForm()
    return render(request, 'classroom/classroom_create.html', {'form': form, 'childcare': childcare})


@login_required
@permission_required_or_403('childcare_employee', (Childcare, 'slug', 'childcare_slug'))
def diary_create(request, childcare_slug):
    childcare = get_object_or_404(Childcare, slug=childcare_slug)
    if request.method == 'POST':
        form = DiaryCreateForm(data=request.POST)
        if form.is_valid():
            try:
                obj = form.save(commit=False)
                obj.author = request.user
                obj.save()
                diary = form.save(commit=True)
                return HttpResponseRedirect('/%s/dashboard/diary/%s' % (childcare_slug, diary.pk))
            except IntegrityError:
                return render(request, 'classroom/error_diary_already_written.html', {'childcare': childcare})
    else:
        form = DiaryCreateForm()
    return render(request, 'classroom/diary_create.html', {'form': form,
                                                           'childcare': childcare})


@login_required
@permission_required_or_403('childcare_view', (Childcare, 'slug', 'childcare_slug'))
def diary_section(request, childcare_slug):
    childcare = get_object_or_404(Childcare, slug=childcare_slug)
    classroom_list = Classroom.objects.filter(childcare=childcare)
    diary_list = Diary.objects.filter(classroom__in=classroom_list)
    return render(request, 'classroom/diary_section.html', {'childcare': childcare,
                                                            'diary_list': diary_list})


@login_required
@permission_required_or_403('childcare_view', (Childcare, 'slug', 'childcare_slug'))
def diary_detail(request, childcare_slug, diary_id):
    childcare = get_object_or_404(Childcare, slug=childcare_slug)
    diary = get_object_or_404(Diary, pk=diary_id)
    return render(request, 'classroom/diary_detail.html', {'childcare': childcare, 'diary': diary})