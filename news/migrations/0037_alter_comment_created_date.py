# Generated by Django 4.2.5 on 2024-09-15 02:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0036_comment_created_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 9, 15, 2, 30, 29, 326805, tzinfo=datetime.timezone.utc)),
        ),
    ]
