from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views.generic.edit import DeleteView, UpdateView
from guardian.decorators import permission_required_or_403
from childcare.models import Childcare
from newsboard.forms import NewsCreateForm, AddNewsImageForm, AddNewsFileForm, NewsUpdateForm
from newsboard.models import News, NewsImage, NewsFile
from django.forms.formsets import formset_factory


@login_required
@permission_required_or_403('childcare_employee', (Childcare, 'slug', 'childcare_slug'))
def childcare_news_create(request, childcare_slug):
    childcare = get_object_or_404(Childcare, slug=childcare_slug)
    if request.method == 'POST':
        form = NewsCreateForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.author = request.user
            obj.childcare = childcare
            obj.save()
            news = form.save(commit=True)
            return HttpResponseRedirect('/%s/dashboard/newsboard/%s' % (childcare_slug, news.pk))
    else:
        form = NewsCreateForm()
    return render(request, 'newsboard/childcare_news_create.html', {'form': form, 'childcare': childcare})


@login_required
@permission_required_or_403('childcare_view', (Childcare, 'slug', 'childcare_slug'))
def childcare_news_detail(request, childcare_slug, news_id):
    childcare = get_object_or_404(Childcare, slug=childcare_slug)
    news = get_object_or_404(News, pk=news_id, childcare=childcare)
    news_image_list = NewsImage.objects.filter(news=news)
    news_file_list = NewsFile.objects.filter(news=news)
    return render(request, 'newsboard/childcare_news_detail.html', {'childcare': childcare,
                                                                    'news': news,
                                                                    'news_image_list': news_image_list,
                                                                    'news_file_list': news_file_list})


@login_required
@permission_required_or_403('childcare_employee', (Childcare, 'slug', 'childcare_slug'))
def childcare_news_update(request, childcare_slug, news_id):
    childcare = get_object_or_404(Childcare, slug=childcare_slug)
    news = get_object_or_404(News, pk=news_id, childcare=childcare)
    if request.method == 'POST':
        form = NewsUpdateForm(data=request.POST, instance=news)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/%s/dashboard/newsboard/%s' % (childcare_slug, news.pk))
    else:
        form = NewsUpdateForm(instance=news)
    return render(request, 'newsboard/childcare_news_update.html', {'form': form,
                                                                    'childcare': childcare,
                                                                    'news': news})


@login_required
@permission_required_or_403('childcare_employee', (Childcare, 'slug', 'childcare_slug'))
def childcare_news_delete(request, childcare_slug, news_id):
    childcare = get_object_or_404(Childcare, slug=childcare_slug)
    news = get_object_or_404(News, pk=news_id, childcare=childcare)
    if request.method == 'POST':
        news.delete()
        return HttpResponseRedirect('/%s/dashboard/newsboard/' % childcare_slug)
    return render(request, 'newsboard/childcare_news_delete.html', {'childcare': childcare,
                                                                    'news': news})


@login_required
@permission_required_or_403('childcare_employee', (Childcare, 'slug', 'childcare_slug'))
def add_news_images(request, childcare_slug, news_id):
    childcare = get_object_or_404(Childcare, slug=childcare_slug)
    news = get_object_or_404(News, pk=news_id)
    ImageFormSet = formset_factory(AddNewsImageForm, extra=5)
    if request.method == 'POST':
        formset = ImageFormSet(request.POST, request.FILES)
        if formset.is_valid():
            for form_image in formset:
                obj = form_image.save(commit=False)
                if obj.image:  # save only forms with images
                    obj.news = news
                    obj.save()
                    form_image.save(commit=True)
            return HttpResponseRedirect('/%s/dashboard/newsboard/%s' % (childcare_slug, news.pk))
    else:
        formset = ImageFormSet()
    return render(request, 'newsboard/add_news_image.html', {'formset': formset,
                                                             'childcare': childcare})


@login_required
@permission_required_or_403('childcare_employee', (Childcare, 'slug', 'childcare_slug'))
def news_image_delete(request, childcare_slug, news_id, image_id):
    childcare = get_object_or_404(Childcare, slug=childcare_slug)
    image = get_object_or_404(NewsImage, pk=image_id, news=news_id)
    news = get_object_or_404(News, pk=news_id)
    if request.method == 'POST':
        image.delete()
        return HttpResponseRedirect('/%s/dashboard/newsboard/%s/' % (childcare_slug, news.pk))
    return render(request, 'newsboard/news_image_delete.html', {'childcare': childcare,
                                                                'image': image})


@login_required
@permission_required_or_403('childcare_employee', (Childcare, 'slug', 'childcare_slug'))
def add_news_files(request, childcare_slug, news_id):
    childcare = get_object_or_404(Childcare, slug=childcare_slug)
    news = get_object_or_404(News, pk=news_id)
    ImageFormSet = formset_factory(AddNewsFileForm, extra=5)
    if request.method == 'POST':
        formset = ImageFormSet(request.POST, request.FILES)
        if formset.is_valid():
            for form_file in formset:
                obj = form_file.save(commit=False)
                if obj.file:  # save only forms with images
                    obj.news = news
                    obj.uploader = request.user
                    obj.save()
                    form_file.save(commit=True)
            return HttpResponseRedirect('/%s/dashboard/newsboard/%s' % (childcare_slug, news.pk))
    else:
        formset = ImageFormSet()
    return render(request, 'newsboard/add_news_file.html', {'formset': formset,
                                                            'childcare': childcare})


@login_required
@permission_required_or_403('childcare_employee', (Childcare, 'slug', 'childcare_slug'))
def news_file_delete(request, childcare_slug, news_id, file_id):
    childcare = get_object_or_404(Childcare, slug=childcare_slug)
    file = get_object_or_404(NewsFile, pk=file_id, news=news_id)
    news = get_object_or_404(News, pk=news_id)
    if request.method == 'POST':
        file.delete()
        return HttpResponseRedirect('/%s/dashboard/newsboard/%s/' % (childcare_slug, news.pk))
    return render(request, 'newsboard/news_file_delete.html', {'childcare': childcare,
                                                               'file': file})


@login_required()
@permission_required_or_403('childcare_view', (Childcare, 'slug', 'childcare_slug'))
def newsboard_section(request, childcare_slug):
    childcare = get_object_or_404(Childcare, slug=childcare_slug)
    news_list = News.objects.filter(childcare=childcare)
    return render(request, 'newsboard/newsboard_section.html', {'childcare': childcare, 'news_list': news_list})