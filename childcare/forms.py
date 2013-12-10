from django.contrib.auth.models import User
from django.forms import ModelForm, ModelMultipleChoiceField, CharField
from .models import Childcare
import autocomplete_light
from utils import autocomplete_light_registry
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
    class Meta:
        model = Childcare
        fields = (
            'description',
        )


class WebsitePageCreateForm(ModelForm):
    content = CharField(widget=CKEditorWidget())

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