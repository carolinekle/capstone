# Generated by Django 4.2.5 on 2024-07-25 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0011_alter_section_url_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='section',
            name='url_name',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]