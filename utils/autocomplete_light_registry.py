import autocomplete_light
from django.contrib.auth.models import User


class UserAutocomplete(autocomplete_light.AutocompleteModelBase):
    search_fields = ['^email', 'username']
    autocomplete_js_attributes = {'placeholder': 'Search by email', }
    model = User

autocomplete_light.register(User, UserAutocomplete)