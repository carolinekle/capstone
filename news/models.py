from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify 
from tinymce.models import HTMLField
from django.utils import timezone

# Create your models here.

class User(AbstractUser):
    pass

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = HTMLField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} Profile'


class Subsection(models.Model):
    subsection_name = models.CharField(max_length=20)
    sub_url_name = models.SlugField(max_length=20, null=True)

    def __str__(self):
        return f"{self.subsection_name}"


class Section(models.Model):
    section_name = models.CharField(max_length=50)
    section_url_name = models.SlugField(max_length=50, null=True, unique=True)

    def __str__(self):
        return f"{self.section_name}"


class Image(models.Model):
    image = models.ImageField(max_length=2000, upload_to="static/news/images")
    caption = models.TextField(max_length=400, null=True, blank=True)


class Author(models.Model):
    byline = models.CharField(max_length=50, null=True)
    author_bio = HTMLField(max_length=2000)
    author_slug = models.SlugField(null=True, blank=True, unique=True)
    pic = models.ForeignKey(Image, null=True, on_delete=models.PROTECT)

    def save(self, *args, **kwargs):
        if not self.author_slug:
            self.author_slug = slugify(self.byline)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.byline}"


class Article(models.Model):
    headline = models.CharField(max_length=50, blank=False, unique_for_date="date")
    main = models.ForeignKey(Image, null=True, on_delete=models.PROTECT)
    byline = models.ForeignKey(Author,null=True, on_delete=models.PROTECT)
    deck = models.CharField(max_length=240, blank=False)
    slug = models.SlugField(unique=True)
    url = models.SlugField(max_length=40, unique=True, null=True)
    date = models.DateTimeField(auto_now_add=False, null=True)
    content = HTMLField()
    section = models.ForeignKey(Section, null=True, on_delete=models.SET_NULL)
    updated_at = models.DateTimeField(blank=True, null=True)
    update_lang = models.CharField(max_length=50, blank=True, null=True)
    is_hero = models.BooleanField(default=False)  
    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.url:
            self.url = slugify(self.headline)
        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.headline} by {self.byline}"
    
    
class Comment(models.Model):
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="commenter")
    comment_text = models.CharField(max_length=240)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, blank=True, null=True, related_name="article")
    created_date = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return f"{self.commenter} commented on {self.article}"
    
    def likes(self):
        return Like.objects.filter(comment_liked=self).count()
    
    def user_likes(self):
        return Like.objects.filter(comment_liked=self).exists()
    
    def since(self):
        return (timezone.now() - self.created_date).days

class Following(models.Model):
    user_following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_following", blank=True, null=True,)
    author_followed = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="author_followed", blank=True, null=True,)

    def __str__(self):
        return f"{self.user_following} is following {self.author_followed}"
    
class Like(models.Model):
    liker = models.ForeignKey(User, on_delete=models.CASCADE, related_name="liker")
    comment_liked = models.ForeignKey(Comment, on_delete=models.CASCADE, blank=True, null=True, related_name="comment_liked")

    def __str__(self):
        return f"User {self.liker} liked {self.comment_liked}"