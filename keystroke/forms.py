from django.forms import ModelForm
from django.forms.models import modelformset_factory

from .models import KeystrokeTestType

class KeystrokeTestTypeForm(ModelForm):

  class Meta:
    model = KeystrokeTestType
    fields = '__all__'
    exclude = ['owner']

KeystrokeTestTypeFormSet = modelformset_factory(KeystrokeTestType, form=KeystrokeTestTypeForm)
