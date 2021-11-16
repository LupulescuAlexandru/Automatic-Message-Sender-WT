from django import forms
from .models import Message


class CreateMessageForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control"}))
    diff_gender = forms.BooleanField(initial=True, required=False,
                                     widget=forms.CheckboxInput(attrs={'class': "form-check"}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}), label="Message")
    message_female = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control'}), label="Message female")

    class Meta:
        model = Message
        fields = '__all__'
        exclude = ['html']


class ChooseFields(forms.Form):
    pass
