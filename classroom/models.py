from django.db import models
from childcare.models import Childcare
from django.contrib.auth.models import User


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


class DiaryImage(models.Model):
    image = models.ImageField(upload_to='images/diary/', null=True)
    #TODO: thumbnail = GalleryThumbnail(source='image')
    diary = models.ForeignKey(Diary, null=True)