from django import forms
from django.forms import ModelForm, TextInput, FileInput, Select, DateInput, RadioSelect
from tinymce.widgets import TinyMCE
from news.models import Article, Author, Image, Section, User
from .models import Homepage

class HomepageForm(forms.ModelForm):
    class Meta:
        model = Homepage
        fields = ['hero_article','featured_articles','featured_404','featured_electric']

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['section','headline', 'main', 'byline', 'deck', 'slug', 'url', 'date', 'content', 'updated_at', 'update_lang', 'is_hero', 'is_featured', 'is_published']
        widgets = {
            'content': TinyMCE(attrs={
                'id': 'content-field',
                'style':"width:70%"
                }),
            'section':Select(attrs={
                'class':"form-select",
                'style':"max-width:300px"
            }),
            'headline': TextInput(attrs={
                'class':"form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Headline'
                 }),
            'deck': TextInput(attrs={
                'class':"form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Deck'
                }),
            'main':Select(attrs={
                'class':"form-select",
                'style':"max-width:300px"
            }),
            'byline':Select(attrs={
                'class':"form-select",
                'style':"max-width:300px"
            }),
            'slug': TextInput(attrs={
                'class':"form-control",
                'style':"max-width:300px",
                }),
            'url':TextInput(attrs={
                'class':"form-control",
                'style':"max-width: 300px",
                'placeholder':"URL"
            }),
            'date': DateInput(attrs={
                'class':"input-group date",
                'style':"max-width: 300px",
            }),
            'is_published':RadioSelect(attrs={
                'class':"form-check-input",
                'id':"flexCheckIndeterminate"
            })
            }

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['byline', 'author_bio','author_slug', 'pic']

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image','caption']

class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ['section_name','section_url_name']

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = "__all__"