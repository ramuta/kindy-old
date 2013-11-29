from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from guardian.decorators import permission_required_or_403
from childcare.forms import ChildcareCreateForm, WebsitePageCreateForm, FirstPageForm, ChooseThemeForm
from childcare.models import Childcare, Theme
from classroom.models import Classroom, DiaryImage, Diary
from newsboard.models import News
from website.models import Page


@login_required
def childcare_create(request):
    if request.method == 'POST':
        form = ChildcareCreateForm(request.POST)
        if form.is_valid():
            #managers = form.cleaned_data['managers']
            childcare = form.save(commit=False)
            # check if there is a default theme
            try:
                theme = get_object_or_404(Theme, pk=1)
                theme_exist = True
            except:
                theme_exist = False
            if theme_exist:
                childcare.theme = get_object_or_404(Theme, pk=1)  # set 1st theme as default
            else:
                theme = Theme(title='Default theme', computer_name='default', description='Default theme')
                theme.save()
                childcare.theme = theme
            childcare = form.save(commit=True)
            # automatically add current user as manager and give him permissions
            childcare.managers.add(request.user)
            managers = list(childcare.managers.all())
            # add manager permissions
            group = Group.objects.get(name='Childcare %s: Manager' % childcare.pk)
            for manager in managers:
                manager.groups.add(group)
            # create default classroom
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


@login_required()
@permission_required_or_403('childcare_view', (Childcare, 'slug', 'childcare_slug'))
def website_section(request, childcare_slug):
    childcare = get_object_or_404(Childcare, slug=childcare_slug)
    website_news_list = News.objects.filter(childcare=childcare, public=True)
    pages_list = Page.objects.filter(childcare=childcare)
    return render(request, 'childcare/website_section.html', {'childcare': childcare,
                                                              'website_news_list': website_news_list,
                                                              'pages_list': pages_list})


@login_required()
@permission_required_or_403('childcare_employee', (Childcare, 'slug', 'childcare_slug'))
def website_page_create(request, childcare_slug):
    childcare = get_object_or_404(Childcare, slug=childcare_slug)
    if request.method == 'POST':
        form = WebsitePageCreateForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.childcare = childcare
            obj.save
            form.save(commit=True)
            return HttpResponseRedirect('/%s/dashboard/website/' % childcare.slug)
    else:
        form = WebsitePageCreateForm()
    return render(request, 'childcare/website_page_create.html', {'form': form, 'childcare': childcare})


@login_required()
@permission_required_or_403('childcare_employee', (Childcare, 'slug', 'childcare_slug'))
def website_first_page_edit(request, childcare_slug):
    childcare = get_object_or_404(Childcare, slug=childcare_slug)
    if request.method == 'POST':
        form = FirstPageForm(request.POST, instance=childcare)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/%s/dashboard/website/' % childcare.slug)
    else:
        form = FirstPageForm(instance=childcare)
    return render(request, 'childcare/first_page_edit.html', {'form': form, 'childcare': childcare})


@login_required
@permission_required_or_403('childcare_employee', (Childcare, 'slug', 'childcare_slug'))
def website_choose_theme(request, childcare_slug):
    childcare = get_object_or_404(Childcare, slug=childcare_slug)
    if request.method == 'POST':
        form = ChooseThemeForm(request.POST, instance=childcare)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/%s/dashboard/website/' % childcare.slug)
    else:
        form = ChooseThemeForm(instance=childcare)
    return render(request, 'childcare/website_choose_theme.html', {'form': form, 'childcare': childcare})


@login_required()
@permission_required_or_403('childcare_view', (Childcare, 'slug', 'childcare_slug'))
def gallery_section(request, childcare_slug):
    childcare = get_object_or_404(Childcare, slug=childcare_slug)
    #news_image_list = News.objects.filter(childcare=childcare)
    classroom_list = Classroom.objects.filter(childcare=childcare)
    diary_list = Diary.objects.filter(classroom_id__in=classroom_list)
    diary_image_list = DiaryImage.objects.filter(diary_id__in=diary_list)
    return render(request, 'childcare/gallery_section.html', {'childcare': childcare,
                                                              'diary_image_list': diary_image_list})