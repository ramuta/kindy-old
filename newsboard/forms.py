from django.forms import ModelForm
from newsboard.models import News, NewsImage, NewsFile


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


class AddNewsFileForm(ModelForm):
    class Meta:
        model = NewsFile
        fields = ('file', 'description',)