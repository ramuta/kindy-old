from django.forms import ModelForm, CharField
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
    description = CharField(required=True)

    class Meta:
        model = NewsFile
        fields = ('file', 'description',)


class NewsUpdateForm(ModelForm):
    class Meta:
        model = News
        fields = ('content', 'public',)