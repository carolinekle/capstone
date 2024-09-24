from django import forms
from django.forms import ModelForm, TextInput, FileInput, Select, DateInput, CheckboxInput, SelectMultiple
from tinymce.widgets import TinyMCE
from .models import Article, Author, Image, Section, User, Like


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','featured_articles','featured_404','featured_electric']
        widgets = {
        }