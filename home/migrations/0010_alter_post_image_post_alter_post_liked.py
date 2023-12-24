# Generated by Django 4.2.7 on 2023-12-19 19:02

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0009_post_image_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image_post',
            field=models.ImageField(upload_to='Image_blog'),
        ),
        migrations.AlterField(
            model_name='post',
            name='liked',
            field=models.ManyToManyField(blank=True, related_name='blog_like', to=settings.AUTH_USER_MODEL),
        ),
    ]