# Generated by Django 4.2.5 on 2024-08-30 00:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0031_remove_article_hero_priority_article_is_featured'),
        ('cms', '0009_remove_homepage_hero_articles_homepage_hero_article'),
    ]

    operations = [
        migrations.RenameField(
            model_name='homepage',
            old_name='hero_article',
            new_name='hero_articles',
        ),
        migrations.RemoveField(
            model_name='homepage',
            name='featured_section',
        ),
        migrations.AddField(
            model_name='homepage',
            name='featured_404',
            field=models.ManyToManyField(related_name='featured_404', to='news.article'),
        ),
    ]