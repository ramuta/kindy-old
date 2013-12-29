from django.db import models
from easy_thumbnails.fields import ThumbnailerField
from easy_thumbnails.files import get_thumbnailer
from childcare.models import Childcare
from django.contrib.auth.models import User
from utils.imagegenerators import get_file_path


class Classroom(models.Model):
    name = models.CharField(max_length=100, blank=True)
    description = models.CharField(max_length=255, blank=True)
    childcare = models.ForeignKey(Childcare, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    modified = models.DateTimeField(auto_now=True, null=True)
    disabled = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return 'childcare/%s/classroom/%s' % (self.childcare.pk, self.pk)


class Diary(models.Model):
    author = models.ForeignKey(User, null=True)
    date = models.DateField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    modified = models.DateTimeField(auto_now=True, null=True)
    classroom = models.ForeignKey(Classroom, null=True)
    content = models.TextField()

    class Meta:
        unique_together = ['classroom', 'date']

    def __unicode__(self):
        return str(self.date)


class DiaryImage(models.Model):
    image = models.ImageField(upload_to=get_file_path, null=True)
    diary = models.ForeignKey(Diary, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    modified = models.DateTimeField(auto_now=True, null=True)
    uploader = models.ForeignKey(User, null=True)