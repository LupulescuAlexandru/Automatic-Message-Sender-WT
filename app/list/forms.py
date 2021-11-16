from django import forms
from .models import List


class DateInput(forms.DateInput):
    input_type = 'date'


class CreateUpdateForm(forms.ModelForm):
    list_types = (
        ("Phone", "Phone"),
        ("Email", "Email"),
        ("Mixt", "Mixt"),
    )

    name = forms.CharField(max_length=100, label="Name", widget=forms.TextInput(attrs={'class': 'form-control'}))
    date = forms.DateField(label="Date", widget=forms.DateInput(format=('%d-%m-%Y'),
                                                                attrs={'class': 'form-control',
                                                                       'placeholder': 'Select a date', 'type': 'date'}))
    reason = forms.CharField(max_length=20, label="Reason", widget=forms.TextInput(attrs={'class': 'form-control'}))
    type = forms.ChoiceField(choices=list_types, label="Type", widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = List
        fields = '__all__'


class CreateListForm(CreateUpdateForm):
    csv_file = forms.FileField(label="CSV File", required=False)

    class Meta:
        model = List
        exclude = ['people']

class UpdateListForm(CreateUpdateForm):
    class Meta:
        model = List
        exclude = ['csv_file']

