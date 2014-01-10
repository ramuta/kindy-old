import datetime
from django.forms.extras.widgets import SelectDateWidget
from classroom.models import Classroom, Diary, DiaryImage
from django.forms import ModelForm, DateField, ModelChoiceField, ValidationError, CharField
from utils.files_images import get_max_size_in_mb, get_max_size


class ClassroomCreateForm(ModelForm):
    class Meta:
        model = Classroom
        fields = (
            'name',
            'description',
        )


class DiaryCreateForm(ModelForm):
    def __init__(self, childcare=None, *args, **kwargs):
        super(DiaryCreateForm, self).__init__(*args, **kwargs)
        self._childcare = childcare
        self.fields['classroom'] = ModelChoiceField(queryset=Classroom.objects.filter(childcare__id=self._childcare.pk,
                                                                                      disabled=False))
    date = DateField(widget=SelectDateWidget, initial=datetime.date.today)

    class Meta:
        model = Diary
        fields = (
            'date',
            'content',
            'classroom',
        )


class AddDiaryImageForm(ModelForm):
    class Meta:
        model = DiaryImage
        fields = ('image',)

    def clean(self):
        cleaned_data = super(AddDiaryImageForm, self).clean()
        image = cleaned_data.get('image')

        if image._size > get_max_size():
            raise ValidationError('Image is too large ( > %s MB )' % get_max_size_in_mb())

        return cleaned_data


class DiaryUpdateForm(ModelForm):
    class Meta:
        model = Diary
        fields = ('content',)


class DiaryImageUpdateForm(ModelForm):
    class Meta:
        model = DiaryImage
        fields = ('image',)