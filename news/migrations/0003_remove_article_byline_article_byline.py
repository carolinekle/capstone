# Generated by Django 4.2.5 on 2024-06-19 18:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("news", "0002_article_author_section_comment_article_byline_and_more"),
    ]

    operations = [
        migrations.RemoveField(model_name="article", name="byline",),
        migrations.AddField(
            model_name="article",
            name="byline",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="news.author",
            ),
        ),
    ]
