# Generated by Django 4.0.5 on 2022-06-25 00:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book_report', '0003_alter_comment_content_alter_comment_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='created at'),
        ),
    ]
