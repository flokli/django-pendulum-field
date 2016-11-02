from django.forms import ModelForm

from .models import User


class PersonForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'creation_date']
