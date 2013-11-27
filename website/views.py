from django.shortcuts import get_object_or_404, render
from childcare.models import Childcare
from newsboard.models import News
from website.models import Page


def website(request, childcare_slug):
    childcare = get_object_or_404(Childcare, slug=childcare_slug)
    #website_news_list = News.objects.filter(childcare=childcare, public=True)
    pages_list = Page.objects.filter(childcare=childcare)
    theme_path = 'themes/'+childcare.theme+'.html'
    return render(request, 'website/website_home.html', {'childcare': childcare,
                                                         #'news_list': website_news_list,
                                                         'pages_list': pages_list,
                                                         'theme_path': theme_path})


def website_news(request, childcare_slug):
    childcare = get_object_or_404(Childcare, slug=childcare_slug)
    website_news_list = News.objects.filter(childcare=childcare, public=True)
    pages_list = Page.objects.filter(childcare=childcare)
    theme_path = 'themes/'+childcare.theme+'.html'
    return render(request, 'website/website_news.html', {'childcare': childcare,
                                                         'news_list': website_news_list,
                                                         'pages_list': pages_list,
                                                         'theme_path': theme_path})


def news_detail(request, childcare_slug, news_slug):
    childcare = get_object_or_404(Childcare, slug=childcare_slug)
    news = get_object_or_404(News, childcare=childcare.pk, slug=news_slug)
    pages_list = Page.objects.filter(childcare=childcare)
    theme_path = 'themes/'+childcare.theme+'.html'
    return render(request, 'website/news_detail.html', {'childcare': childcare,
                                                        'news': news,
                                                        'pages_list': pages_list,
                                                        'theme_path': theme_path})


def page_detail(request, childcare_slug, page_slug):
    childcare = get_object_or_404(Childcare, slug=childcare_slug)
    page = get_object_or_404(Page, childcare=childcare.pk, slug=page_slug)
    pages_list = Page.objects.filter(childcare=childcare)
    theme_path = 'themes/'+childcare.theme+'.html'
    return render(request, 'website/page_detail.html', {'childcare': childcare,
                                                        'page': page,
                                                        'pages_list': pages_list,
                                                        'theme_path': theme_path})