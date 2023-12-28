# Generated by Django 4.2.7 on 2023-12-23 17:00

import django.core.validators
from django.db import migrations, models
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='default.jpg', upload_to='profile_pics', validators=[django.core.validators.FileExtensionValidator(['png', 'jpg', 'jpeg']), users.models.validate_file_mime_type]),
        ),
    ]