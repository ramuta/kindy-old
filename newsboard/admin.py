from django.contrib import admin
from newsboard.models import News, NewsImage, NewsFile

admin.site.register(News)
admin.site.register(NewsImage)
admin.site.register(NewsFile)