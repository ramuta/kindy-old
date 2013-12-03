from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.core.urlresolvers import reverse_lazy
from django.forms.formsets import formset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views.generic.edit import DeleteView, UpdateView
from guardian.decorators import permission_required_or_403
from childcare.models import Childcare
from classroom.forms import ClassroomCreateForm, DiaryCreateForm, AddDiaryImageForm, DiaryUpdateForm
from classroom.models import Classroom, Diary, DiaryImage
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
    diary_list = Diary.objects.filter(classroom__in=classroom_list)
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
                    obj.save()
                    form_image.save(commit=True)
            return HttpResponseRedirect('/%s/dashboard/diary/%s' % (childcare_slug, diary.pk))
    else:
        formset = ImageFormSet()
    return render(request, 'classroom/add_diary_image.html', {'formset': formset,
                                                              'childcare': childcare})


'''Delete/update views'''


class DiaryDelete(DeleteView):
    model = Diary
    template_name = 'classroom/diary_delete.html'

    def get_context_data(self, **kwargs):
        context = super(DiaryDelete, self).get_context_data(**kwargs)
        context['childcare'] = self.object.classroom.childcare
        return context

    def get_success_url(self):
        return '/%s/dashboard/diary/' % self.object.classroom.childcare.slug


class DiaryUpdate(UpdateView):
    model = Diary
    form_class = DiaryUpdateForm
    template_name = 'classroom/diary_update.html'

    def get_context_data(self, **kwargs):
        context = super(DiaryUpdate, self).get_context_data(**kwargs)
        context['childcare'] = self.object.classroom.childcare
        return context