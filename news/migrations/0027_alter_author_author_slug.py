# Generated by Django 4.2.5 on 2024-08-19 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0026_author_author_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='author_slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
    ]
