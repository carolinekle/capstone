# Generated by Django 4.2.5 on 2024-09-15 01:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0035_remove_like_article_liked_like_comment_liked'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='created_date',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
