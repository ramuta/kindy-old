from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from guardian.decorators import permission_required_or_403
from childcare.models import Childcare
from newsboard.forms import NewsCreateForm, AddNewsImageForm, AddNewsFileForm, NewsUpdateForm
from newsboard.models import News, NewsImage, NewsFile
from django.forms.formsets import formset_factory
from utils.files_images import get_max_size_in_mb
from utils.imagegenerators import utils_generate_thumbnail

# setup logging
import logging
log = logging.getLogger("logentries")
log_prefix = '[kindylog]'


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
            log.info(log_prefix+'News created (childcare: %s, user: %s)' % (childcare.name, request.user))
            return HttpResponseRedirect(reverse('childcare:news_detail', kwargs={'childcare_slug': childcare.slug,
                                                                               'news_id': news.pk}))
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
            log.info(log_prefix+'News updated (childcare: %s, user: %s)' % (childcare.name, request.user))
            return HttpResponseRedirect(reverse('childcare:news_detail', kwargs={'childcare_slug': childcare.slug,
                                                                                 'news_id': news.pk}))
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
        log.info(log_prefix+'News deleted (childcare: %s, user: %s)' % (childcare.name, request.user))
        return HttpResponseRedirect(reverse('childcare:news_list', kwargs={'childcare_slug': childcare.slug}))
    return render(request, 'newsboard/childcare_news_delete.html', {'childcare': childcare,
                                                                    'news': news})


@login_required
@permission_required_or_403('childcare_employee', (Childcare, 'slug', 'childcare_slug'))
def add_news_images(request, childcare_slug, news_id):
    childcare = get_object_or_404(Childcare, slug=childcare_slug)
    news = get_object_or_404(News, pk=news_id)
    image_size = get_max_size_in_mb()
    if request.method == 'POST':
        form = AddNewsImageForm(request.POST, request.FILES)
        if form.is_valid():
            log.info(log_prefix+'News images added (childcare: %s, user: %s)' % (childcare.name, request.user))
            obj = form.save(commit=False)
            if obj.image:  # save only forms with images
                obj.news = news
                obj.uploader = request.user
                obj.save()
                object = form.save(commit=True)
                # generate thumbnail
                utils_generate_thumbnail(object)
                return HttpResponseRedirect(reverse('childcare:news_detail', kwargs={'childcare_slug': childcare.slug,
                                                                                 'news_id': news.pk}))
    else:
        form = AddNewsImageForm()
    return render(request, 'newsboard/add_news_image.html', {'form': form,
                                                             'childcare': childcare,
                                                             'image_size': image_size})


@login_required
@permission_required_or_403('childcare_employee', (Childcare, 'slug', 'childcare_slug'))
def news_image_delete(request, childcare_slug, news_id, image_id):
    childcare = get_object_or_404(Childcare, slug=childcare_slug)
    image = get_object_or_404(NewsImage, pk=image_id, news=news_id)
    news = get_object_or_404(News, pk=news_id)
    if request.method == 'POST':
        image.delete()
        log.info(log_prefix+'News image deleted (childcare: %s, user: %s)' % (childcare.name, request.user))
        return HttpResponseRedirect(reverse('childcare:news_detail', kwargs={'childcare_slug': childcare.slug,
                                                                             'news_id': news.pk}))
    return render(request, 'newsboard/news_image_delete.html', {'childcare': childcare,
                                                                'image': image})


@login_required
@permission_required_or_403('childcare_employee', (Childcare, 'slug', 'childcare_slug'))
def add_news_files(request, childcare_slug, news_id):
    childcare = get_object_or_404(Childcare, slug=childcare_slug)
    news = get_object_or_404(News, pk=news_id)
    file_size = get_max_size_in_mb()
    if request.method == 'POST':
        form = AddNewsFileForm(request.POST, request.FILES)
        if form.is_valid():
            log.info(log_prefix+'News files added (childcare: %s, user: %s)' % (childcare.name, request.user))
            obj = form.save(commit=False)
            if obj.file:  # save only forms with files
                obj.news = news
                obj.uploader = request.user
                obj.save()
                form.save(commit=True)
                return HttpResponseRedirect(reverse('childcare:news_detail', kwargs={'childcare_slug': childcare.slug,
                                                                                     'news_id': news.pk}))
    else:
        form = AddNewsFileForm()
    return render(request, 'newsboard/add_news_file.html', {'form': form,
                                                            'childcare': childcare,
                                                            'file_size': file_size})


@login_required
@permission_required_or_403('childcare_employee', (Childcare, 'slug', 'childcare_slug'))
def news_file_delete(request, childcare_slug, news_id, file_id):
    childcare = get_object_or_404(Childcare, slug=childcare_slug)
    file = get_object_or_404(NewsFile, pk=file_id, news=news_id)
    news = get_object_or_404(News, pk=news_id)
    if request.method == 'POST':
        file.delete()
        log.info(log_prefix+'News file deleted (childcare: %s, user: %s)' % (childcare.name, request.user))
        return HttpResponseRedirect(reverse('childcare:news_detail', kwargs={'childcare_slug': childcare.slug,
                                                                             'news_id': news.pk}))
    return render(request, 'newsboard/news_file_delete.html', {'childcare': childcare,
                                                               'file': file})


@login_required()
@permission_required_or_403('childcare_view', (Childcare, 'slug', 'childcare_slug'))
def newsboard_section(request, childcare_slug):
    childcare = get_object_or_404(Childcare, slug=childcare_slug)
    all_news_list = News.objects.filter(childcare=childcare)
    log.info(log_prefix+'Newsboard (childcare: %s, user: %s)' % (childcare.name, request.user))

    paginator = Paginator(all_news_list, 10)
    page = request.GET.get('page')

    try:
        news_list = paginator.page(page)
    except PageNotAnInteger:
        news_list = paginator.page(1)
    except EmptyPage:
        news_list = paginator.page(paginator.num_pages)

    return render(request, 'newsboard/newsboard_section.html', {'childcare': childcare, 'news_list': news_list})