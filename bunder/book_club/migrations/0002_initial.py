# Generated by Django 4.0.5 on 2022-06-23 10:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('book_club', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='bookclubmember',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='유저 ID'),
        ),
        migrations.AddField(
            model_name='bookclubbooks',
            name='club',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book_club.bookclub', verbose_name='소모임 ID'),
        ),
        migrations.AddField(
            model_name='bookclub',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='북클럽장'),
        ),
    ]