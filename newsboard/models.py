from django.contrib.auth.models import User
from django.db import models
from childcare.models import Childcare
from django.template.defaultfilters import slugify


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
            self.slug = slugify(self.title)
        super(News, self).save(*args, **kwargs)


class NewsImage(models.Model):
    image = models.ImageField(upload_to='images/news/', blank=True)
    news = models.ForeignKey(News)
    #created


class NewsFile(models.Model):
    file = models.FileField(upload_to='files/news/')
    description = models.CharField(max_length=500, blank=True)
    uploader = models.ForeignKey(User)
    news = models.ForeignKey(News)
    #created