# Generated by Django 4.0.5 on 2022-06-20 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_alter_user_nickname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='categories',
            field=models.CharField(choices=[('문학', '문학'), ('경제/경영', '경제/경영'), ('자기계발', '자기계발'), ('인문', '인문'), ('정치/사회', '정치/사회'), ('예술', '예술'), ('과학', '과학'), ('기술/IT', '기술/IT')], max_length=64),
        ),
    ]