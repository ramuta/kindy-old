from django.forms import ModelForm, CharField, ValidationError, BooleanField
from newsboard.models import News, NewsImage, NewsFile
from utils.files_images import get_max_size, get_max_size_in_mb


class NewsCreateForm(ModelForm):
    public = BooleanField(label='Public (visible on website)', initial=False, required=False)

    class Meta:
        model = News
        fields = ('title',
                  'content',
                  'public',)


class AddNewsImageForm(ModelForm):
    class Meta:
        model = NewsImage
        fields = ('image',)

    def clean(self):
        cleaned_data = super(AddNewsImageForm, self).clean()
        image = cleaned_data.get('image')

        if image:
            if image._size > get_max_size():
                raise ValidationError('Image is too large ( > %s MB )' % get_max_size_in_mb())
        else:
            raise ValidationError('Image field must not be empty.')

        return cleaned_data


class AddNewsFileForm(ModelForm):
    description = CharField(required=True)

    class Meta:
        model = NewsFile
        fields = ('file', 'description',)

    def clean(self):
        cleaned_data = super(AddNewsFileForm, self).clean()
        news_file = cleaned_data.get('file')

        if news_file:
            if news_file._size > get_max_size():
                raise ValidationError('File is too large ( > %s MB )' % get_max_size_in_mb())
        else:
            raise ValidationError('File field must not be empty.')

        return cleaned_data


class NewsUpdateForm(ModelForm):
    class Meta:
        model = News
        fields = ('content', 'public',)