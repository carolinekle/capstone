# Generated by Django 4.2.5 on 2024-07-29 18:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0017_alter_section_sub_sections'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='section',
            name='sub_sections',
        ),
    ]