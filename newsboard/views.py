from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from guardian.decorators import permission_required_or_403
from childcare.models import Childcare
from newsboard.forms import NewsCreateForm, AddNewsImageForm
from newsboard.models import News, NewsImage
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
    return render(request, 'newsboard/childcare_news_detail.html', {'childcare': childcare,
                                                                    'news': news,
                                                                    'news_image_list': news_image_list})


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


@login_required()
@permission_required_or_403('childcare_view', (Childcare, 'slug', 'childcare_slug'))
def newsboard_section(request, childcare_slug):
    childcare = get_object_or_404(Childcare, slug=childcare_slug)
    news_list = News.objects.filter(childcare=childcare)
    return render(request, 'newsboard/newsboard_section.html', {'childcare': childcare, 'news_list': news_list})