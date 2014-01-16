from django.contrib.auth.models import Group, User
from django.db import models
from utils.roles import roles_childcare_init_new
from utils.slugify import unique_slugify
from localflavor.us import models as usmodels


# create default theme in admin when syncdb
class Theme(models.Model):
    title = models.CharField(max_length=255, unique=True)
    computer_name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    preview = models.ImageField(upload_to='images/themes/', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.title

    def get_computer_name(self):
        return self.computer_name


class Childcare(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(verbose_name='URL', unique=True, max_length=100, null=True)
    logo = models.ImageField(upload_to='images/logos/', blank=True, null=True)
    slogan = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    street_address = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=100, null=True)
    state = usmodels.USStateField(blank=True, choices=usmodels.STATE_CHOICES, null=True)
    managers = models.ManyToManyField(User, related_name='childcare_managers', null=True)
    employees = models.ManyToManyField(User, related_name='childcare_employees', blank=True)
    parents = models.ManyToManyField(User, related_name='childcare_parents', blank=True)
    theme = models.ForeignKey(Theme, null=True)
    website_image = models.CharField(max_length=100, blank=True, default='default')
    email = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=100, blank=True, null=True)
    disabled = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

    class Meta:
        permissions = (
            ('childcare_view', 'View childcare dashboard'),
            ('childcare_employee', 'Updating childcare content'),
            ('childcare_admin', 'Childcare administration'),
        )

    def save(self, *args, **kwargs):
        is_create = False
        if not self.id:
            is_create = True

        if not self.slug:
            self.slug = unique_slugify(self, self.name)

        super(Childcare, self).save(*args, **kwargs)

        if is_create:
            roles_childcare_init_new(self)

    def get_absolute_url(self):
        return '/childcare/%s' % self.id


class GroupChildcare(models.Model):
    childcare = models.ForeignKey(Childcare)
    group = models.ForeignKey(Group)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return u"%s" % self.group.name

    class Meta:
        unique_together = ['childcare', 'group']