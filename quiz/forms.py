from django.forms import ModelForm
from django.forms.models import modelformset_factory

from .models import Quiz

class QuizForm(ModelForm):

  class Meta:
    model = Quiz
    fields = '__all__'
    exclude = ['quiz_owner']

QuizFormSet = modelformset_factory(Quiz, form=QuizForm)
