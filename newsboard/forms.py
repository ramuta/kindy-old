from django.forms import ModelForm
from newsboard.models import News, NewsImage


class NewsCreateForm(ModelForm):
    class Meta:
        model = News
        fields = ('title',
                  'content',
                  'public',)


class AddNewsImageForm(ModelForm):
    class Meta:
        model = NewsImage
        fields = ('image',)