from django import forms
from django.forms import ModelForm, TextInput, FileInput, Select, DateInput, CheckboxInput, SelectMultiple
from tinymce.widgets import TinyMCE
from news.models import Article, Author, Image, Section, User, Like
from .models import Homepage

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
        fields = ['headline','deck','section','byline','main','content', 'slug', 'url', 'date', 'is_published', 'updated_at', 'update_lang']
        widgets = {
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
                    'id':"id_main",
                    'class':"form-select",
                    'style':"max-width:300px"
                }),
                'byline':Select(attrs={
                    'class':"form-select",
                    'style':"max-width:300px"
                }),
                'content': TinyMCE(attrs={
                    'id': 'content-field',
                    'class':":form-control"
                    }),
                'section':Select(attrs={
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
                    'class':"input-group rounded-1 border border-1 p-1",
                    'style':"max-width: 300px",
                    'type':"date"
                }),
                'is_published':CheckboxInput(attrs={
                    'class':"form-check-input",
                    'id':"flexCheckDefault",
                    'type':"checkbox"
                }),
                'updated_at':DateInput(attrs={
                    'class':"input-group rounded-1 border border-1 p-1",
                    'style':"max-width: 300px",
                    'type':"date"
                }),
                'update_lang':TextInput(attrs={
                    'class':"form-control",
                    'style': 'max-width: 300px;',
                    'placeholder': 'Update Language'
                }),
                }
        
        def __init__(self, *args, **kwargs):
            super(ArticleForm, self).__init__(*args, **kwargs)
            images = Image.objects.all()
            self.fields['main'].choices = [(image.pk, image.name) for image in images]

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
        fields = ['name','image','caption']
        widgets={
            'name':TextInput(attrs={
                'class':"form-control",
                'style': 'max-width: 300px;',
            }),
            'image':FileInput(attrs={
                'type':"file",
                'class':"form-control",
                'name':"image",
                'id':"imageInput",
                'accept':"image/*"
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