from django.contrib.auth.models import User
from django.db import models, IntegrityError
from childcare.models import Childcare
from utils.imagegenerators import get_file_path
from utils.slugify import unique_slugify


class News(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    created = models.DateTimeField(auto_now_add=True)  # null=True
    modified = models.DateTimeField(auto_now=True)  # null=True
    author = models.ForeignKey(User)
    content = models.TextField()
    childcare = models.ForeignKey(Childcare)
    public = models.BooleanField(default=False)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['-created']

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = unique_slugify(self, self.title)
        super(News, self).save(*args, **kwargs)


class NewsImage(models.Model):
    image = models.ImageField(upload_to=get_file_path, blank=True)
    thumbnail = models.CharField(max_length=255, null=True)
    news = models.ForeignKey(News)
    created = models.DateTimeField(auto_now_add=True, null=True)
    modified = models.DateTimeField(auto_now=True, null=True)
    uploader = models.ForeignKey(User, null=True)


class NewsFile(models.Model):
    file = models.FileField(upload_to=get_file_path)
    description = models.CharField(max_length=500, blank=True)
    uploader = models.ForeignKey(User)
    news = models.ForeignKey(News)
    created = models.DateTimeField(auto_now_add=True, null=True)
    modified = models.DateTimeField(auto_now=True, null=True)