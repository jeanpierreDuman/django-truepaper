from .models import *
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms


class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class ArticleForm(ModelForm):

    class Meta:
        model = Article
        fields = ['title', 'hang', 'category', 'time', 'decision', 'youtube', 'text', 'haveImage']


class ComponentForm(ModelForm):
    class Meta:
        model = Component
        fields = ['component']


class ParameterForm(ModelForm):
    class Meta:
        model = Parameter
        fields = ['secretQuestion', 'secretResponse']


class CommentaryForm(ModelForm):
    class Meta:
        model = Commentary
        fields = ['comment']


class JustificationForm(ModelForm):
    class Meta:
        model = Justification
        fields = ['decision', 'text']


class FactForm(ModelForm):
    class Meta:
        model = Fact
        fields = ['text']