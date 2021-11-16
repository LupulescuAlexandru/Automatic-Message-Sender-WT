from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={'style': "width:100%;"}))
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'style': "width:100%;"}))
