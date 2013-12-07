import datetime
from django.forms.extras.widgets import SelectDateWidget
from classroom.models import Classroom, Diary, DiaryImage
from django.forms import ModelForm, DateField, ModelChoiceField


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
        self.fields['classroom'] = ModelChoiceField(queryset=Classroom.objects.filter(childcare__id=self._childcare.pk))
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


class DiaryUpdateForm(ModelForm):
    class Meta:
        model = Diary
        fields = ('content',)


class DiaryImageUpdateForm(ModelForm):
    class Meta:
        model = DiaryImage
        fields = ('image',)