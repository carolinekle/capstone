# Generated by Django 4.2.5 on 2024-09-20 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0042_alter_article_is_featured_alter_article_is_hero_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='section',
            name='section_description',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]
