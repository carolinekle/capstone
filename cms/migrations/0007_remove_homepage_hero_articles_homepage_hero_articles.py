# Generated by Django 4.2.5 on 2024-08-29 23:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0031_remove_article_hero_priority_article_is_featured'),
        ('cms', '0006_remove_homepage_featured_err_homepage_featured_404_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='homepage',
            name='hero_articles',
        ),
        migrations.AddField(
            model_name='homepage',
            name='hero_articles',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='hero_articles', to='news.article'),
        ),
    ]
