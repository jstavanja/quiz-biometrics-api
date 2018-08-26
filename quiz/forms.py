from django.forms import ModelForm
from django.forms.models import modelformset_factory

from .models import Quiz
from keystroke.models import KeystrokeTestType

class QuizForm(ModelForm):

  def __init__(self, *args, **kwargs):
    self.user = kwargs.pop('owner')
    super(QuizForm, self).__init__(*args, **kwargs)

  class Meta:
    model = Quiz
    fields = '__all__'
    exclude = ['course']

QuizFormSet = modelformset_factory(Quiz, form=QuizForm)
