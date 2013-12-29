from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.forms.formsets import formset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from guardian.decorators import permission_required_or_403
from childcare.models import Childcare
from classroom.forms import ClassroomCreateForm, DiaryCreateForm, AddDiaryImageForm, DiaryUpdateForm
from classroom.models import Classroom, Diary, DiaryImage
from django.db import IntegrityError
from utils.imagegenerators import utils_generate_thumbnail


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
        form = DiaryCreateForm(data=request.POST, childcare=childcare)
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
        form = DiaryCreateForm(childcare=childcare)
    return render(request, 'classroom/diary_create.html', {'form': form,
                                                           'childcare': childcare})


@login_required
@permission_required_or_403('childcare_view', (Childcare, 'slug', 'childcare_slug'))
def diary_section(request, childcare_slug):
    childcare = get_object_or_404(Childcare, slug=childcare_slug)
    classroom_list = Classroom.objects.filter(childcare=childcare)
    all_diary_list = Diary.objects.filter(classroom__in=classroom_list).order_by('-date')

    paginator = Paginator(all_diary_list, 10)
    page = request.GET.get('page')

    try:
        diary_list = paginator.page(page)
    except PageNotAnInteger:
        diary_list = paginator.page(1)
    except EmptyPage:
        diary_list = paginator.page(paginator.num_pages)

    return render(request, 'classroom/diary_section.html', {'childcare': childcare,
                                                            'diary_list': diary_list})


@login_required
@permission_required_or_403('childcare_view', (Childcare, 'slug', 'childcare_slug'))
def diary_detail(request, childcare_slug, diary_id):
    childcare = get_object_or_404(Childcare, slug=childcare_slug)
    diary = get_object_or_404(Diary, pk=diary_id)
    diary_image_list = DiaryImage.objects.filter(diary=diary)
    return render(request, 'classroom/diary_detail.html', {'childcare': childcare,
                                                           'diary': diary,
                                                           'diary_image_list': diary_image_list})


@login_required
@permission_required_or_403('childcare_employee', (Childcare, 'slug', 'childcare_slug'))
def diary_update(request, childcare_slug, diary_id):
    childcare = get_object_or_404(Childcare, slug=childcare_slug)
    diary = get_object_or_404(Diary, pk=diary_id)
    #ImageFormSet = formset_factory(DiaryImageUpdateForm, )
    if request.method == 'POST':
        form = DiaryUpdateForm(data=request.POST, instance=diary)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/%s/dashboard/diary/%s/' % (childcare_slug, diary.pk))
    else:
        form = DiaryUpdateForm(instance=diary)
    return render(request, 'classroom/diary_update.html', {'form': form,
                                                           'childcare': childcare,
                                                           'diary': diary})


@login_required
@permission_required_or_403('childcare_employee', (Childcare, 'slug', 'childcare_slug'))
def diary_delete(request, childcare_slug, diary_id):
    childcare = get_object_or_404(Childcare, slug=childcare_slug)
    diary = get_object_or_404(Diary, pk=diary_id)
    if request.method == 'POST':
        diary.delete()
        return HttpResponseRedirect('/%s/dashboard/diary/' % childcare_slug)
    return render(request, 'classroom/diary_delete.html', {'childcare': childcare,
                                                           'diary': diary})


@login_required
@permission_required_or_403('childcare_employee', (Childcare, 'slug', 'childcare_slug'))
def add_diary_images(request, childcare_slug, diary_id):
    childcare = get_object_or_404(Childcare, slug=childcare_slug)
    diary = get_object_or_404(Diary, pk=diary_id)
    ImageFormSet = formset_factory(AddDiaryImageForm, extra=5)
    if request.method == 'POST':
        formset = ImageFormSet(request.POST, request.FILES)
        if formset.is_valid():
            for form_image in formset:
                obj = form_image.save(commit=False)
                if obj.image:  # save only forms with images
                    obj.diary = diary
                    obj.uploader = request.user
                    obj.save()
                    object = form_image.save(commit=True)
                    # generate thumbnail
                    utils_generate_thumbnail(object)
            return HttpResponseRedirect('/%s/dashboard/diary/%s/' % (childcare_slug, diary.pk))
    else:
        formset = ImageFormSet()
    return render(request, 'classroom/add_diary_image.html', {'formset': formset,
                                                              'childcare': childcare})


@login_required
@permission_required_or_403('childcare_employee', (Childcare, 'slug', 'childcare_slug'))
def diary_image_delete(request, childcare_slug, diary_id, image_id):
    childcare = get_object_or_404(Childcare, slug=childcare_slug)
    diary_image = get_object_or_404(DiaryImage, pk=image_id, diary=diary_id)
    diary = get_object_or_404(Diary, pk=diary_id)
    if request.method == 'POST':
        diary_image.delete()
        return HttpResponseRedirect('/%s/dashboard/diary/%s/' % (childcare_slug, diary.pk))
    return render(request, 'classroom/diary_image_delete.html', {'childcare': childcare,
                                                                 'image': diary_image})


@login_required
@permission_required_or_403('childcare_view', (Childcare, 'slug', 'childcare_slug'))
def classroom_list(request, childcare_slug):
    childcare = get_object_or_404(Childcare, slug=childcare_slug)
    all_classroom_list = Classroom.objects.filter(childcare=childcare, disabled=False)

    paginator = Paginator(all_classroom_list, 10)
    page = request.GET.get('page')

    try:
        classroom_list = paginator.page(page)
    except PageNotAnInteger:
        classroom_list = paginator.page(1)
    except EmptyPage:
        classroom_list = paginator.page(paginator.num_pages)

    return render(request, 'classroom/classroom_list.html', {'childcare': childcare,
                                                             'classroom_list': classroom_list})


@login_required
@permission_required_or_403('childcare_employee', (Childcare, 'slug', 'childcare_slug'))
def classroom_delete(request, childcare_slug, classroom_id):
    childcare = get_object_or_404(Childcare, slug=childcare_slug)
    classroom = get_object_or_404(Classroom, pk=classroom_id)
    if request.method == 'POST':
        classroom.disabled = True
        classroom.save()
        return HttpResponseRedirect('/%s/dashboard/classroom/' % childcare_slug)
    return render(request, 'classroom/classroom_delete.html', {'childcare': childcare,
                                                               'classroom': classroom})


@login_required
@permission_required_or_403('childcare_employee', (Childcare, 'slug', 'childcare_slug'))
def classroom_update(request, childcare_slug, classroom_id):
    childcare = get_object_or_404(Childcare, slug=childcare_slug)
    classroom = get_object_or_404(Classroom, pk=classroom_id)
    if request.method == 'POST':
        form = ClassroomCreateForm(data=request.POST, instance=classroom)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/%s/dashboard/classroom' % childcare_slug)
    else:
        form = ClassroomCreateForm(instance=classroom)
    return render(request, 'classroom/classroom_update.html', {'childcare': childcare,
                                                               'classroom': classroom,
                                                               'form': form})