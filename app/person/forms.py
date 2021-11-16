from django import forms
from django.core.validators import RegexValidator

from .models import Person

phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                             message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")


class CreateUpdatePersonForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control"}))
    gender = forms.Select()
    phone = forms.CharField(required=False, validators=[phone_regex], widget=forms.TextInput(attrs={'class': "form-control"}))
    email = forms.CharField(required=False, widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Person
        fields = '__all__'
