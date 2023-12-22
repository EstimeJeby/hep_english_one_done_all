# Generated by Django 4.2.7 on 2023-12-02 17:26

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0004_alter_comment_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='liked',
            field=models.ManyToManyField(blank=True, related_name='Blog_post', to=settings.AUTH_USER_MODEL),
        ),
    ]
