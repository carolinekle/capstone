from django.contrib import admin
from .models import User, Section, Article, Author, Comment, Image, Following, Profile


# Register your models here.
admin.site.register(User)

admin.site.register(Article)
admin.site.register(Author)
admin.site.register(Section)
admin.site.register(Comment)
admin.site.register(Image)
admin.site.register(Following)
admin.site.register(Profile)
