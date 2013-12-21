from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify
from childcare.models import Childcare
from utils.imagegenerators import get_file_path


class Page(models.Model):
    title = models.CharField(max_length=100, blank=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    modified = models.DateTimeField(auto_now=True, null=True)
    content = models.TextField(null=True)
    childcare = models.ForeignKey(Childcare, null=True)
    order = models.SmallIntegerField(default=1, null=True)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['order']

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title)
        super(Page, self).save(*args, **kwargs)


class PageFile(models.Model):
    file = models.FileField(upload_to=get_file_path, null=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    uploader = models.ForeignKey(User, null=True)
    page = models.ForeignKey(Page, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)