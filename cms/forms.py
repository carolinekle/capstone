from django import forms
from django.forms import ModelForm, TextInput, FileInput, Select, DateInput, CheckboxInput, SelectMultiple
from tinymce.widgets import TinyMCE
from news.models import Article, Author, Image, Section, User, Like
from .models import Homepage
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Div, Field


class HomepageForm(forms.ModelForm):
    class Meta:
        model = Homepage
        fields = ['hero_article','featured_articles','featured_404','featured_electric']
        widgets = {
            'hero_article':Select(attrs={
                'class':"form-select",
                'style':"max-width:300px"
            }),
            'featured_articles':SelectMultiple(attrs={
                'class':"form-select",
                'style':"max-width:300px"
            }),
            'featured_404':SelectMultiple(attrs={
                'class':"form-select",
                'style':"max-width:300px"
            }),
            'featured_electric':SelectMultiple(attrs={
                'class':"form-select",
                'style':"max-width:300px"
            }),
        }


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article  
        fields = ['content', 'section', 'headline', 'deck', 'main', 'byline', 'slug', 'url', 'date', 'is_published', 'updated_at', 'update_lang']

        widgets = {
            'content': TinyMCE(),  
        }

        def __init__(self, *args, **kwargs):
            super(ArticleForm, self).__init__(*args, **kwargs)
            self.helper1 = FormHelper()
            self.helper1.form_method = 'post'
            self.helper1.layout = Layout(
                Div(
                    Field('headline', css_class="form-control", style="max-width: 300px;", placeholder='Headline'),
                    Field('byline', css_class="form-select", style="max-width:300px"),
                    Field('deck', css_class="form-control", style="max-width: 300px;", placeholder='Deck'),
                    Field('main', css_class="form-select", style="max-width:300px"),
                    Field('content'),
                    Field('is_published', template='bootstrap5/checkbox.html'),
                    Submit('submit', 'Save')
                )
            )

            self.helper2 = FormHelper()
            self.helper2.form_tag = False
            self.helper2.form_method = 'post'
            self.helper2.layout = Layout(
                Div(
                    Field('section', css_class="form-select", style="max-width:300px"),
                    Field('slug', css_class="form-control", style="max-width:300px"),
                    Field('url', css_class="form-control", style="max-width:300px", placeholder='URL'),
                    Field('updated_at', css_class="input-group", style="max-width:300px", type="date"),
                    Field('update_lang', css_class="form-control", style="max-width: 300px;", placeholder='Update Language'),
                )
            )

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['byline', 'author_bio','author_slug', 'pic']
        widgets= {
            'byline':TextInput(attrs={
                'class':"form-control",
                'style': 'max-width: 300px;',
            }),
            'author_bio':TinyMCE(attrs={
                'id': 'content-field',
                'class':":form-control"
            }),
            'author_slug':TextInput(attrs={
                'class':"form-control",
                'style': 'max-width: 300px;',
            }),
            'pic':Select(attrs={
                'class':"form-select",
                'style':"max-width:300px"
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['byline'].label = "Author's name"
        self.fields['author_slug'].label = "URL"

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image','caption']
        widgets={
            'image':FileInput(attrs={
                'type':"file",
                'class':"form-control" 
            }),
            'caption':TextInput(attrs={
                'class':"form-control",
                'style': 'max-width: 300px;',
            })
        }

class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ['section_name','section_url_name']
        widgets={
            'section_name':TextInput(attrs={
                'class':"form-control",
                'style': 'max-width: 300px;',
            }),
            'section_url_name':TextInput(attrs={
                'class':"form-control",
                'style': 'max-width: 300px;',
            })
        }

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = "__all__"