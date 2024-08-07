from django import forms
from news.models import Article, Author, Image, Section

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['headline', 'main', 'byline', 'deck', 'slug', 'url', 'date', 'content', 'section', 'updated_at', 'update_lang', 'is_hero', 'hero_priority', 'is_published']

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['author', 'author_bio']

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image','caption']

class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ['section_name','section_url_name']