import datetime
from django.forms.extras.widgets import SelectDateWidget
from classroom.models import Classroom, Diary, DiaryImage
from django.forms import ModelForm, DateField


class ClassroomCreateForm(ModelForm):
    class Meta:
        model = Classroom
        fields = (
            'name',
            'description',
        )


class DiaryCreateForm(ModelForm):
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