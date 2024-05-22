from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):
    pass


class Section(models.Model):
    section_name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.section_name}"
    
class Author(models.Model):
    author = models.CharField(max_length=50)
    author_bio = models.CharField(max_length=2000)

    def __str__(self):
        return f"{self.author}"


class Article(models.Model):
    headline = models.CharField(max_length=50, blank=False, unique_for_date="date", unique_for_date="slug")
    image = models.CharField(max_length=2000)
    byline = models.ForeignKey(Author)
    deck = models.CharField(max_length=240, blank=False)
    slug = models.SlugField(unique=True)
    date = models.DateTimeField(auto_now_add=True)
    content = models.CharField(blank=False)
    section = models.ForeignKey(Section)
    update_lang = models.DateTimeField(blank=True)

    def __str__(self):
        return f"{self.headline} by {self.author}"
    
    
class Comment(models.Model):
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user")
    comment_text = models.CharField(max_length=240)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, blank=True, null=True, related_name="article")
    
    def __str__(self):
        return f"{self.commenter} comment on ({self.listing})"