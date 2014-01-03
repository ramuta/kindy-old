from itertools import chain
from operator import attrgetter
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from guardian.decorators import permission_required_or_403
from childcare.forms import ChildcareCreateForm, WebsitePageCreateForm, FirstPageForm, ChooseThemeForm, ManagersAddForm, EmployeesAddForm, ParentsAddForm, AddPageFileForm, ChildcareUpdateForm, InviteUsersForm
from childcare.models import Childcare, Theme
from classroom.models import Classroom, DiaryImage, Diary
from newsboard.models import News, NewsImage
from utils.invites import invite_new_kindy_user
from website.models import Page, PageFile
from django.forms.formsets import formset_factory

# setup logging
import logging
log = logging.getLogger("logentries")


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
            log.info('Childcare created (childcare: %s, user: %s)' % (childcare.name, request.user))
            return HttpResponseRedirect('/%s/dashboard/' % childcare.slug)
    else:
        form = ChildcareCreateForm()
    return render(request, 'childcare/childcare_create.html', {'form': form})


@login_required()
@permission_required_or_403('childcare_employee', (Childcare, 'slug', 'childcare_slug'))
def childcare_update(request, childcare_slug):
    childcare = get_object_or_404(Childcare, slug=childcare_slug)
    if request.method == 'POST':
        form = ChildcareUpdateForm(data=request.POST, instance=childcare)
        if form.is_valid():
            form.save()
            log.info('Childcare updated (childcare: %s, user: %s)' % (childcare.name, request.user))
            return HttpResponseRedirect('/%s/dashboard/' % childcare.slug)
    else:
        form = ChildcareUpdateForm(instance=childcare)
    return render(request, 'childcare/childcare_update.html', {'form': form,
                                                               'childcare': childcare})


@login_required
@permission_required_or_403('childcare_view', (Childcare, 'slug', 'childcare_slug'))
def childcare(request, childcare_slug):
    childcare = get_object_or_404(Childcare, slug=childcare_slug)
    log.info('Childcare opened (childcare: %s, user: %s)' % (childcare.name, request.user))
    classroom_num = Classroom.objects.filter(childcare=childcare, disabled=False).count()
    manager_num = User.objects.filter(childcare_managers__id=childcare.pk).count()
    employee_num = User.objects.filter(childcare_employees__id=childcare.pk).count()
    parent_num = User.objects.filter(childcare_parents__id=childcare.pk).count()

    classroom_list = Classroom.objects.filter(childcare=childcare)
    diary_num = Diary.objects.filter(classroom__in=classroom_list).count()

    news_num = News.objects.filter(childcare=childcare).count()
    return render(request, 'childcare/childcare_detail.html', {'childcare': childcare,
                                                               'classroom_num': classroom_num,
                                                               'manager_num': manager_num,
                                                               'employee_num': employee_num,
                                                               'parent_num': parent_num,
                                                               'diary_num': diary_num,
                                                               'news_num': news_num})


@login_required()
@permission_required_or_403('childcare_view', (Childcare, 'slug', 'childcare_slug'))
def website_section(request, childcare_slug):
    childcare = get_object_or_404(Childcare, slug=childcare_slug)
    log.info('Childcare Website section (%s)' % childcare.name)
    website_news_list = News.objects.filter(childcare=childcare, public=True)[:5]
    pages_list = Page.objects.filter(childcare=childcare)[:5]
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
            log.info('Page created (childcare: %s, user: %s)' % (childcare.name, request.user))
            return HttpResponseRedirect('/%s/dashboard/page/%s/' % (childcare.slug, obj.pk))
    else:
        form = WebsitePageCreateForm()
    return render(request, 'childcare/website_page_create.html', {'form': form, 'childcare': childcare})


@login_required
@permission_required_or_403('childcare_view', (Childcare, 'slug', 'childcare_slug'))
def website_page_detail(request, childcare_slug, page_id):
    childcare = get_object_or_404(Childcare, slug=childcare_slug)
    page = get_object_or_404(Page, pk=page_id, childcare=childcare)
    log.info('Page detail (%s: %s)' % (childcare.name, page.title))
    page_file_list = PageFile.objects.filter(page=page)
    return render(request, 'childcare/website_page_detail.html', {'childcare': childcare,
                                                                  'page': page,
                                                                  'page_file_list': page_file_list})


@login_required()
@permission_required_or_403('childcare_employee', (Childcare, 'slug', 'childcare_slug'))
def website_page_update(request, childcare_slug, page_id):
    childcare = get_object_or_404(Childcare, slug=childcare_slug)
    page = get_object_or_404(Page, pk=page_id, childcare=childcare)
    if request.method == 'POST':
        form = WebsitePageCreateForm(data=request.POST, instance=page)
        if form.is_valid():
            form.save()
            log.info('Page updated (%s: %s, user: %s)' % (childcare.name, page.title, request.user))
            return HttpResponseRedirect('/%s/dashboard/page/%s/' % (childcare.slug, page.pk))
    else:
        form = WebsitePageCreateForm(instance=page)
    return render(request, 'childcare/website_page_update.html', {'form': form,
                                                                  'childcare': childcare,
                                                                  'page': page})


@login_required()
@permission_required_or_403('childcare_employee', (Childcare, 'slug', 'childcare_slug'))
def website_page_delete(request, childcare_slug, page_id):
    childcare = get_object_or_404(Childcare, slug=childcare_slug)
    page = get_object_or_404(Page, pk=page_id, childcare=childcare)
    if request.method == 'POST':
        page.delete()
        log.info('Page deleted (childcare: %s, user: %s)' % (childcare.name, request.user))
        return HttpResponseRedirect('/%s/dashboard/pages/' % childcare.slug)
    return render(request, 'childcare/website_page_delete.html', {'childcare': childcare,
                                                                  'page': page})


@login_required
@permission_required_or_403('childcare_view', (Childcare, 'slug', 'childcare_slug'))
def website_pages_list(request, childcare_slug):
    childcare = get_object_or_404(Childcare, slug=childcare_slug)
    all_page_list = Page.objects.filter(childcare=childcare)

    paginator = Paginator(all_page_list, 10)
    page = request.GET.get('page')

    try:
        page_list = paginator.page(page)
    except PageNotAnInteger:
        page_list = paginator.page(1)
    except EmptyPage:
        page_list = paginator.page(paginator.num_pages)

    return render(request, 'childcare/website_page_list.html', {'childcare': childcare,
                                                                'page_list': page_list})


@login_required
@permission_required_or_403('childcare_employee', (Childcare, 'slug', 'childcare_slug'))
def add_page_files(request, childcare_slug, page_id):
    childcare = get_object_or_404(Childcare, slug=childcare_slug)
    page = get_object_or_404(Page, pk=page_id)
    FileFormSet = formset_factory(AddPageFileForm, extra=5)
    if request.method == 'POST':
        formset = FileFormSet(request.POST, request.FILES)
        if formset.is_valid():
            log.info('Page files added (childcare: %s, user: %s)' % (childcare.name, request.user))
            for form_file in formset:
                obj = form_file.save(commit=False)
                if obj.file:  # save only forms with files
                    obj.page = page
                    obj.uploader = request.user
                    obj.save()
                    form_file.save(commit=True)
                    return HttpResponseRedirect('/%s/dashboard/page/%s' % (childcare_slug, page.pk))
    else:
        formset = FileFormSet()
    return render(request, 'childcare/add_page_file.html', {'formset': formset,
                                                            'childcare': childcare})


@login_required
@permission_required_or_403('childcare_employee', (Childcare, 'slug', 'childcare_slug'))
def page_file_delete(request, childcare_slug, page_id, file_id):
    childcare = get_object_or_404(Childcare, slug=childcare_slug)
    file = get_object_or_404(PageFile, pk=file_id, page=page_id)
    page = get_object_or_404(Page, pk=page_id)
    if request.method == 'POST':
        file.delete()
        log.info('Page file deleted (childcare: %s, user: %s)' % (childcare.name, request.user))
        return HttpResponseRedirect('/%s/dashboard/page/%s/' % (childcare_slug, page.pk))
    return render(request, 'childcare/page_file_delete.html', {'childcare': childcare,
                                                               'file': file})


@login_required()
@permission_required_or_403('childcare_employee', (Childcare, 'slug', 'childcare_slug'))
def website_first_page_edit(request, childcare_slug):
    childcare = get_object_or_404(Childcare, slug=childcare_slug)
    if request.method == 'POST':
        form = FirstPageForm(request.POST, instance=childcare)
        if form.is_valid():
            form.save()
            log.info('About edited (childcare: %s, user: %s)' % (childcare.name, request.user))
            return HttpResponseRedirect('/%s/dashboard/pages/' % childcare.slug)
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
            log.info('Theme changed (childcare: %s, user: %s)' % (childcare.name, request.user))
            return HttpResponseRedirect('/%s/dashboard/pages/' % childcare.slug)
    else:
        form = ChooseThemeForm(instance=childcare)
    return render(request, 'childcare/website_choose_theme.html', {'form': form, 'childcare': childcare})


@login_required()
@permission_required_or_403('childcare_view', (Childcare, 'slug', 'childcare_slug'))
def gallery_section(request, childcare_slug):
    childcare = get_object_or_404(Childcare, slug=childcare_slug)
    classroom_list = Classroom.objects.filter(childcare=childcare)
    diary_list = Diary.objects.filter(classroom_id__in=classroom_list)
    news_list = News.objects.filter(childcare=childcare)
    diary_image_list = DiaryImage.objects.filter(diary_id__in=diary_list)
    news_image_list = NewsImage.objects.filter(news_id__in=news_list)
    all_image_list = list(chain(diary_image_list, news_image_list))
    all_image_list.sort(key=attrgetter('created'), reverse=True)
    log.info('Gallery (childcare: %s, user: %s)' % (childcare.name, request.user))

    paginator = Paginator(all_image_list, 60)
    page = request.GET.get('page')

    try:
        image_list = paginator.page(page)
    except PageNotAnInteger:
        image_list = paginator.page(1)
    except EmptyPage:
        image_list = paginator.page(paginator.num_pages)

    return render(request, 'childcare/gallery_section.html', {'childcare': childcare,
                                                              'image_list': image_list})


@login_required()
@permission_required_or_403('childcare_admin', (Childcare, 'slug', 'childcare_slug'))
def managers_add_remove(request, childcare_slug):
    childcare = get_object_or_404(Childcare, slug=childcare_slug)
    if request.method == 'POST':
        form = ManagersAddForm(request.POST, instance=childcare)
        if form.is_valid():
            old_managers = list(childcare.managers.all())  # have to convert to list to preserve values in it
            new_managers = form.cleaned_data['managers']
            form.save(commit=True)
            log.info('Managers added/removed (childcare: %s, user: %s)' % (childcare.name, request.user))
            group = Group.objects.get(name='Childcare %s: Manager' % childcare.pk)
            for user in new_managers:
                user.groups.add(group)
            for old_user in old_managers:
                if old_user not in new_managers:
                    old_user.groups.remove(group)
            return HttpResponseRedirect('/%s/dashboard/managers/' % childcare.slug)
    else:
        form = ManagersAddForm(instance=childcare)
    return render(request, 'childcare/managers_add.html', {'form': form, 'childcare': childcare})


@login_required()
@permission_required_or_403('childcare_employee', (Childcare, 'slug', 'childcare_slug'))
def employees_add_remove(request, childcare_slug):
    childcare = get_object_or_404(Childcare, slug=childcare_slug)
    if request.method == 'POST':
        form = EmployeesAddForm(request.POST, instance=childcare)
        if form.is_valid():
            old_employees = list(childcare.employees.all())  # have to convert to list to preserve values in it
            new_employees = form.cleaned_data['employees']
            form.save(commit=True)
            group = Group.objects.get(name='Childcare %s: Employee' % childcare.pk)
            log.info('Employees added/removed (childcare: %s, user: %s)' % (childcare.name, request.user))
            for user in new_employees:
                user.groups.add(group)
            for old_user in old_employees:
                if old_user not in new_employees:
                    old_user.groups.remove(group)
            return HttpResponseRedirect('/%s/dashboard/employees/' % childcare.slug)
    else:
        form = EmployeesAddForm(instance=childcare)
    return render(request, 'childcare/employees_add.html', {'form': form, 'childcare': childcare})


@login_required()
@permission_required_or_403('childcare_employee', (Childcare, 'slug', 'childcare_slug'))
def parents_add_remove(request, childcare_slug):
    childcare = get_object_or_404(Childcare, slug=childcare_slug)
    if request.method == 'POST':
        form = ParentsAddForm(request.POST, instance=childcare)
        if form.is_valid():
            old_parents = list(childcare.parents.all())  # have to convert to list to preserve values in it
            new_parents = form.cleaned_data['parents']
            form.save(commit=True)
            group = Group.objects.get(name='Childcare %s: Parent' % childcare.pk)
            log.info('Parents added/removed (childcare: %s, user: %s)' % (childcare.name, request.user))
            for user in new_parents:
                user.groups.add(group)
            for old_user in old_parents:
                if old_user not in new_parents:
                    old_user.groups.remove(group)
            return HttpResponseRedirect('/%s/dashboard/parents/' % childcare.slug)
    else:
        form = ParentsAddForm(instance=childcare)
    return render(request, 'childcare/parents_add.html', {'form': form, 'childcare': childcare})


@login_required()
@permission_required_or_403('childcare_view', (Childcare, 'slug', 'childcare_slug'))
def managers_list(request, childcare_slug):
    childcare = get_object_or_404(Childcare, slug=childcare_slug)
    all_managers_list = childcare.managers.all()

    paginator = Paginator(all_managers_list, 10)
    page = request.GET.get('page')

    try:
        managers_list = paginator.page(page)
    except PageNotAnInteger:
        managers_list = paginator.page(1)
    except EmptyPage:
        managers_list = paginator.page(paginator.num_pages)
    return render(request, 'childcare/managers_list.html', {'childcare': childcare,
                                                            'managers_list': managers_list})


@login_required()
@permission_required_or_403('childcare_view', (Childcare, 'slug', 'childcare_slug'))
def employees_list(request, childcare_slug):
    childcare = get_object_or_404(Childcare, slug=childcare_slug)

    all_employees_list = childcare.employees.all()

    paginator = Paginator(all_employees_list, 10)
    page = request.GET.get('page')

    try:
        employees_list = paginator.page(page)
    except PageNotAnInteger:
        employees_list = paginator.page(1)
    except EmptyPage:
        employees_list = paginator.page(paginator.num_pages)
    return render(request, 'childcare/employees_list.html', {'childcare': childcare,
                                                             'employees_list': employees_list})


@login_required()
@permission_required_or_403('childcare_view', (Childcare, 'slug', 'childcare_slug'))
def parents_list(request, childcare_slug):
    childcare = get_object_or_404(Childcare, slug=childcare_slug)
    all_parents_list = childcare.parents.all()

    paginator = Paginator(all_parents_list, 10)
    page = request.GET.get('page')

    try:
        parents_list = paginator.page(page)
    except PageNotAnInteger:
        parents_list = paginator.page(1)
    except EmptyPage:
        parents_list = paginator.page(paginator.num_pages)
    return render(request, 'childcare/parents_list.html', {'childcare': childcare,
                                                           'parents_list': parents_list})


@login_required()
@permission_required_or_403('childcare_employee', (Childcare, 'slug', 'childcare_slug'))
def invite_users(request, childcare_slug):
    childcare = get_object_or_404(Childcare, slug=childcare_slug)
    if request.method == 'POST':
        form = InviteUsersForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data[u'first_name']  # .encode('ascii')
            last_name = form.cleaned_data[u'last_name']
            email = form.cleaned_data['email']
            role = form.cleaned_data['role']
            inviter = request.user
            invite_new_kindy_user(email=email,
                                  first_name=first_name,
                                  last_name=last_name,
                                  inviter=inviter,
                                  childcare=childcare,
                                  role=role)
            log.info('User invited (childcare: %s, user: %s)' % (childcare.name, request.user))
            return HttpResponseRedirect('/%s/dashboard/' % childcare.slug)
    else:
        form = InviteUsersForm()
    return render(request, 'childcare/invite_users.html', {'form': form, 'childcare': childcare})