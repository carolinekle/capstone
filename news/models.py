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
    author_bio = models.TextField(max_length=2000)

    def __str__(self):
        return f"{self.author}"

class Image(models.Model):
    image = models.ImageField(max_length=2000, upload_to="static/news/images")
    caption = models.TextField(max_length=400, null=True, blank=True)

# image
class Article(models.Model):
    headline = models.CharField(max_length=50, blank=False, unique_for_date="date")
    main = models.ManyToManyField(Image)
    byline = models.ForeignKey(Author,null=True, on_delete=models.SET_NULL)
    deck = models.CharField(max_length=240, blank=False)
    slug = models.SlugField(unique=True)
    date = models.DateTimeField(auto_now_add=True)
    content = models.TextField(blank=False, max_length=10000)
    section = models.ManyToManyField(Section)
    update_lang = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.headline} by {self.byline}"
    
    
class Comment(models.Model):
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="commenter")
    comment_text = models.CharField(max_length=240)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, blank=True, null=True, related_name="article")
    
    def __str__(self):
        return f"{self.commenter} comment on ({self.article})"