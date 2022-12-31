from django.forms import ModelForm
from models import *


class InputForm(ModelForm):
    class Meta:
        model = CreateInput
        fields = '__all__'



