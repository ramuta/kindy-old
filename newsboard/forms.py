from django.forms import ModelForm
from newsboard.models import News


class NewsCreateForm(ModelForm):
    class Meta:
        model = News
        fields = ('title',
                  'content',
                  'public',)