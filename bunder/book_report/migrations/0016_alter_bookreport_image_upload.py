# Generated by Django 4.0.5 on 2022-06-28 17:18

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book_report', '0015_alter_comment_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookreport',
            name='image_upload',
            field=models.ImageField(blank=True, null=True, upload_to='book_report_images', validators=[django.core.validators.FileExtensionValidator(['jpg', 'png', 'jpeg', 'gif', 'bmp', 'webp'])]),
        ),
    ]
