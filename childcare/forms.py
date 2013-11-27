from django.contrib.auth.models import User
from django.forms import ModelForm, ModelMultipleChoiceField
from .models import Childcare
import autocomplete_light
from utils import autocomplete_light_registry


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