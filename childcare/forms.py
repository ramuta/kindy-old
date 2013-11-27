from django.contrib.auth.models import User
from django.forms import ModelForm, ModelMultipleChoiceField
from .models import Childcare
import autocomplete_light
from utils import autocomplete_light_registry
from website.models import Page


class ChildcareCreateForm(ModelForm):
    managers = ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=autocomplete_light.MultipleChoiceWidget('UserAutocomplete'))

    class Meta:
        model = Childcare
        fields = ('name',
                  'slug',
                  'street_address',
                  'city',
                  'managers',)
        exclude = ('disabled',)


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