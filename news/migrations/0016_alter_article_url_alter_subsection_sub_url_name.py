# Generated by Django 4.2.5 on 2024-07-29 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0015_alter_section_section_url_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='url',
            field=models.SlugField(max_length=40, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='subsection',
            name='sub_url_name',
            field=models.SlugField(max_length=20, null=True),
        ),
    ]