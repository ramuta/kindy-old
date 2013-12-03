from django.contrib.auth.models import User
from django.forms import ModelForm, ModelMultipleChoiceField
from .models import Childcare
import autocomplete_light
from utils import autocomplete_light_registry
from website.models import Page, PageFile


class ChildcareCreateForm(ModelForm):
    '''
    def __init__(self, user=None, *args, **kwargs):
        super(ChildcareCreateForm, self).__init__(*args, **kwargs)
        self.managers = user

    managers = ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=autocomplete_light.MultipleChoiceWidget('UserAutocomplete'))
    '''
    class Meta:
        model = Childcare
        fields = ('name',
                  'slug',
                  'street_address',
                  'city',)
        exclude = ('disabled', 'managers',)


class FirstPageForm(ModelForm):
    class Meta:
        model = Childcare
        fields = (
            'description',
        )


class WebsitePageCreateForm(ModelForm):
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
    class Meta:
        model = PageFile
        fields = ('file', 'description',)