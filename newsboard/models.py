from django.contrib.auth.models import User
from django.db import models, IntegrityError
import re
from childcare.models import Childcare
from django.template.defaultfilters import slugify
from utils.imagegenerators import get_file_path


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
        #As long as this object does NOT have a slug
        if not self.slug:
            from django.template.defaultfilters import slugify
            #Take the title and replace spaces with hypens, make lowercase
            potential_slug = slugify(self.title)
            self.slug = potential_slug

            while True:
                try:
                    #try to save the object
                    super(News, self).save(*args, **kwargs)

                #if this slug already exists we get an error
                except IntegrityError:
                    #match the slug or look for a trailing number
                    match_obj = re.match(r'^(.*)-(\d+)$', self.slug)

                    #if we find a match
                    if match_obj:
                        #take the found number and increment it by 1
                        next_int = int(match_obj.group(2)) + 1
                        self.slug = match_obj.group(1) + "-" + str(next_int)
                    else:
                        #There are no matches for -# so create one with -2
                        self.slug += '-2'
                #different error than IntegrityError
                else:
                    break
        super(News, self).save(*args, **kwargs)


class NewsImage(models.Model):
    image = models.ImageField(upload_to=get_file_path, blank=True)
    news = models.ForeignKey(News)
    #created


class NewsFile(models.Model):
    file = models.FileField(upload_to=get_file_path)
    description = models.CharField(max_length=500, blank=True)
    uploader = models.ForeignKey(User)
    news = models.ForeignKey(News)
    #created