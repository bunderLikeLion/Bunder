# Generated by Django 4.0.5 on 2022-06-20 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_alter_user_categories'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='nickname',
            field=models.CharField(max_length=32, verbose_name='닉네임'),
        ),
    ]
