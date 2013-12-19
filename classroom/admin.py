from django.contrib import admin
from classroom.models import Diary, Classroom, DiaryImage


class DiaryAdmin(admin.ModelAdmin):
    list_filter = ['created', 'classroom', 'author']
    list_display = ['classroom', 'date', 'author']


class ClassroomAdmin(admin.ModelAdmin):
    list_filter = ['created', 'childcare']
    list_display = ['name', 'childcare', 'created']

admin.site.register(Diary, DiaryAdmin)
admin.site.register(Classroom, ClassroomAdmin)
admin.site.register(DiaryImage)