# Generated by Django 4.2.5 on 2024-09-09 19:30

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0032_alter_article_update_lang'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='author_bio',
            field=tinymce.models.HTMLField(max_length=2000),
        ),
        migrations.AlterField(
            model_name='profile',
            name='bio',
            field=tinymce.models.HTMLField(blank=True, null=True),
        ),
    ]