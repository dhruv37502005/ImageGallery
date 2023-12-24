from cProfile import label
from tkinter import Image
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Images

from .models import Images

class ImageForm(forms.ModelForm):
    class Meta:
        model = Images
        fields = "__all__"
        labels = {"photo": ""}


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
