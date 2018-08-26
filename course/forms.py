from django.forms import ModelForm
from django.forms.models import modelformset_factory

from .models import Course
from quiz.models import Quiz
from keystroke.models import KeystrokeTestType

class CourseForm(ModelForm):

  def __init__(self, *args, **kwargs):
    self.user = kwargs.pop('owner')
    super(CourseForm, self).__init__(*args, **kwargs)
    self.fields['keystroke_test_type'].queryset = KeystrokeTestType.objects.filter(owner=self.user)

  class Meta:
    model = Course
    fields = '__all__'
    exclude = ['owner']

CourseFormSet = modelformset_factory(Course, form=CourseForm)
