# Generated by Django 4.2.5 on 2024-07-29 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0014_remove_section_url_name_article_url_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='section',
            name='section_url_name',
            field=models.SlugField(null=True),
        ),
    ]
