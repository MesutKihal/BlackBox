
from django import forms
from . import models as md

class AddUser(forms.Form):
    username = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'input'}))
    email = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'input'}))
    password = forms.CharField(label="", widget=forms.PasswordInput(attrs={'class': 'input'}))
    confirm = forms.CharField(label="", widget=forms.PasswordInput(attrs={'class': 'input'}))
    class Meta:
        model = md.User
        fields = ['username', 'email', 'password']

class LogUser(forms.Form):
    username = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'input'}))
    password = forms.CharField(label="", widget=forms.PasswordInput(attrs={'class': 'input'}))