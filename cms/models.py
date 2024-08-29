from django.db import models
from news.models import Article, Section

# Create your models here.
class Homepage(models.Model):
    hero_articles = models.ManyToManyField(Article, related_name="hero_articles")
    featured_articles = models.ManyToManyField(Article, related_name="featured_articles")
    date_created = models.DateTimeField(auto_now_add=True)

    def get_featured_by_section(self, section):
        return self.featured_articles.filter(section=section)

    def __str__(self):
        return f"Homepage on {self.date_created}"