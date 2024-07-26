from django.contrib import admin
from .models import User, Section, Article, Author, Comment, Image


# Register your models here.
admin.site.register(User)


class ArticleAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("headline",)}
    list_display = ('headline', 'date', 'updated_at')


admin.site.register(Article, ArticleAdmin)
admin.site.register(Author)
admin.site.register(Section)
admin.site.register(Comment)
admin.site.register(Image)
