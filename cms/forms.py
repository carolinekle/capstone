from django import forms
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
        fields = ['headline', 'main', 'byline', 'deck', 'slug', 'url', 'date', 'content', 'section', 'updated_at', 'update_lang', 'is_hero', 'is_featured', 'is_published']
        widgets = {'content': TinyMCE(attrs={'id': 'content-field','cols': 80, 'rows': 30})}

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