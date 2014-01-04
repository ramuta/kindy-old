from django.shortcuts import get_object_or_404, render
from childcare.models import Childcare
from newsboard.models import News, NewsImage, NewsFile
from website.models import Page, PageFile

# setup logging
import logging
log = logging.getLogger("logentries")

log_prefix = '[kindylog]'


def website(request, childcare_slug):
    childcare = get_object_or_404(Childcare, slug=childcare_slug)
    website_news_list = News.objects.filter(childcare=childcare, public=True)
    pages_list = Page.objects.filter(childcare=childcare)
    log.info(log_prefix+'Website index (childcare: %s)' % childcare.name)
    return render(request, 'themes/'+childcare.theme.computer_name+'/index.html', {'childcare': childcare,
                                                                                   'news_list': website_news_list,
                                                                                   'pages_list': pages_list})


def website_news(request, childcare_slug):
    childcare = get_object_or_404(Childcare, slug=childcare_slug)
    website_news_list = News.objects.filter(childcare=childcare, public=True)
    pages_list = Page.objects.filter(childcare=childcare)
    log.info(log_prefix+'Website news list (childcare: %s)' % childcare.name)
    return render(request, 'themes/'+childcare.theme.computer_name+'/news_list.html', {'childcare': childcare,
                                                                                       'news_list': website_news_list,
                                                                                       'pages_list': pages_list})


def news_detail(request, childcare_slug, news_slug):
    childcare = get_object_or_404(Childcare, slug=childcare_slug)
    news = get_object_or_404(News, childcare=childcare.pk, slug=news_slug)
    pages_list = Page.objects.filter(childcare=childcare)
    news_image_list = NewsImage.objects.filter(news=news)
    news_file_list = NewsFile.objects.filter(news=news)
    log.info(log_prefix+'Website news detail (childcare: %s)' % childcare.name)
    return render(request, 'themes/'+childcare.theme.computer_name+'/news_detail.html', {'childcare': childcare,
                                                                                         'news': news,
                                                                                         'pages_list': pages_list,
                                                                                         'news_image_list': news_image_list,
                                                                                         'news_file_list': news_file_list})


def page_detail(request, childcare_slug, page_slug):
    childcare = get_object_or_404(Childcare, slug=childcare_slug)
    page = get_object_or_404(Page, childcare=childcare.pk, slug=page_slug)
    pages_list = Page.objects.filter(childcare=childcare)
    page_file_list = PageFile.objects.filter(page=page)
    log.info(log_prefix+'Website page detail (childcare: %s)' % childcare.name)
    return render(request, 'themes/'+childcare.theme.computer_name+'/page_detail.html', {'childcare': childcare,
                                                                                         'page': page,
                                                                                         'pages_list': pages_list,
                                                                                         'page_file_list': page_file_list})


def about(request, childcare_slug):
    childcare = get_object_or_404(Childcare, slug=childcare_slug)
    pages_list = Page.objects.filter(childcare=childcare)
    log.info(log_prefix+'Website about (childcare: %s)' % childcare.name)
    return render(request, 'themes/'+childcare.theme.computer_name+'/about.html', {'childcare': childcare,
                                                                                   'pages_list': pages_list})