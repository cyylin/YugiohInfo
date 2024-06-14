from django import forms
from msite import models

class LoginForm(forms.Form):
    Account = forms.CharField(label='帳號', max_length=20, widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete':'off'}))
    Password = forms.CharField(label='密碼', widget=forms.PasswordInput(attrs={'class': 'form-control'}))