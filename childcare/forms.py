from django.contrib.auth.models import User
from django.forms import ModelForm, ModelMultipleChoiceField, CharField, EmailField, Form, ChoiceField, Select, ValidationError
from userena.forms import SignupForm
from .models import Childcare
import autocomplete_light
from utils import autocomplete_light_registry
from utils.files_images import get_max_size, get_max_size_in_mb
from utils.slugify import get_forbidden_words_list
from website.models import Page, PageFile
from ckeditor.widgets import CKEditorWidget


class ChildcareCreateForm(ModelForm):
    class Meta:
        model = Childcare
        fields = ('name',
                  'slug',
                  'street_address',
                  'city',)
        exclude = ('disabled', 'managers',)

    def clean(self):
        cleaned_data = super(ChildcareCreateForm, self).clean()
        slug = cleaned_data.get('slug')

        if slug in get_forbidden_words_list():
            raise ValidationError('This URL is not available. Please choose another one.')

        return cleaned_data


class ChildcareUpdateForm(ModelForm):
    class Meta:
        model = Childcare
        fields = ('name',
                  'slug',
                  'slogan',
                  'street_address',
                  'city',
                  'state',
                  'email',
                  'phone_number',)


class FirstPageForm(ModelForm):
    description = CharField(widget=CKEditorWidget(config_name='custom'))

    class Meta:
        model = Childcare
        fields = (
            'description',
        )


class WebsitePageCreateForm(ModelForm):
    content = CharField(widget=CKEditorWidget(config_name='custom'))
    CHOICES = (('1', '1',), ('2', '2',), ('3', '3',), ('4', '4',), ('5', '5',), ('6', '6',), ('7', '7',), ('8', '8',), ('9', '9',), ('10', '10',),)
    order = ChoiceField(widget=Select, choices=CHOICES)

    class Meta:
        model = Page
        fields = ('title',
                  'content',
                  'order',)


class ChooseThemeForm(ModelForm):
    class Meta:
        model = Childcare
        fields = (
            'theme',
        )


class ManagersAddForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ManagersAddForm, self).__init__(*args, **kwargs)
        self.fields['managers'] = ModelMultipleChoiceField(
            queryset=User.objects.all(),
            widget=autocomplete_light.MultipleChoiceWidget('UserAutocomplete'))

    class Meta:
        model = Childcare
        fields = (
            'managers',
        )


class EmployeesAddForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(EmployeesAddForm, self).__init__(*args, **kwargs)
        self.fields['employees'] = ModelMultipleChoiceField(
            queryset=User.objects.all(),
            widget=autocomplete_light.MultipleChoiceWidget('UserAutocomplete'))

    class Meta:
        model = Childcare
        fields = (
            'employees',
        )


class ParentsAddForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ParentsAddForm, self).__init__(*args, **kwargs)
        self.fields['parents'] = ModelMultipleChoiceField(
            queryset=User.objects.all(),
            widget=autocomplete_light.MultipleChoiceWidget('UserAutocomplete'))

    class Meta:
        model = Childcare
        fields = (
            'parents',
        )


class AddPageFileForm(ModelForm):
    description = CharField(required=True)

    class Meta:
        model = PageFile
        fields = ('file', 'description',)

    def clean(self):
        cleaned_data = super(AddPageFileForm, self).clean()
        file = cleaned_data.get('file')

        if file._size > get_max_size():
            raise ValidationError('File is too large ( > %s MB )' % get_max_size_in_mb())

        return cleaned_data


ROLE_CHOICES_MANAGER = (
    ('Parent', 'Parent'),
    ('Employee', 'Employee'),
    ('Manager', 'Manager'),
)

ROLE_CHOICES_EMPLOYEE = (
    ('Parent', 'Parent'),
    ('Employee', 'Employee'),
)


class InviteUsersForm(Form):
    first_name = CharField(max_length=200, required=True)
    last_name = CharField(max_length=200, required=True)
    email = EmailField(required=True)
    role = ChoiceField(choices=ROLE_CHOICES_EMPLOYEE, required=True)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.childcare = kwargs.pop('childcare', None)
        super(InviteUsersForm, self).__init__(*args, **kwargs)

        if self.request.user in self.childcare.managers.all():
            self.fields['role'] = ChoiceField(choices=ROLE_CHOICES_MANAGER, required=True)
        else:
            self.fields['role'] = ChoiceField(choices=ROLE_CHOICES_EMPLOYEE, required=True)

    def clean(self):
        email = self.cleaned_data['email']
        role = self.cleaned_data['role']

        user = None

        try:
            user = User.objects.get(email=email)

            if user in self.childcare.managers.all() and role == 'Manager':
                raise ValidationError(u'This user is already a manager in your childcare.')
            elif user in self.childcare.employees.all() and role == 'Employee':
                raise ValidationError(u'This user is already an employee in your childcare.')
            elif user in self.childcare.parents.all() and role == 'Parent':
                raise ValidationError(u'This user is already a parent in your childcare.')
            return self.cleaned_data
        except user.DoesNotExist:
            return self.cleaned_data