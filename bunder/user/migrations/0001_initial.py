# Generated by Django 4.0.5 on 2022-06-19 13:22

import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('userid', models.CharField(max_length=32, unique=True, verbose_name='아이디')),
                ('password', models.CharField(max_length=32, verbose_name='비밀번호')),
                ('nickname', models.CharField(max_length=32, unique=True, verbose_name='닉네임')),
                ('age', models.IntegerField(verbose_name='나이')),
                ('categories', models.CharField(choices=[('ANTIQUES & COLLECTIBLES', '엔틱 & 수집서적'), ('ART', '예술'), ('DESIGN', '디자인'), ('PHOTOGRAPHY', '사진'), ('BIOGRAPHY & AUTOBIOGRAPHY', '자서전'), ('BUSINESS & ECONOMICS', '경제 / 경영'), ('JUVENILE FICTION', '청소년 문학소설'), ('JUVENILE NONFICTION', '청소년 산문문학'), ('COMICS & GRAPHIC NOVELS', '만화 / 그래픽노블'), ('COMPUTERS', '컴퓨터'), ('TRANSPORTATION', '교통'), ('COOKING', '요리'), ('CRAFTS & HOBBIES', '공예 / 취미'), ('EDUCATION', '교육'), ('FOREIGN LANGUAGE STUDY', '외국어'), ('LANGUAGE ARTS & DISCIPLINES', '언어예술 및 규율'), ('LITERARY COLLECTIONS', '문학선집'), ('LITERARY CRITICISM', '문학비판'), ('MATHEMATICS', '수학'), ('STUDY AIDS', '학습자료'), ('ARCHITECTURE', '건축'), ('TECHNOLOGY & ENGINEERING', '기술 / 공학'), ('DRAMA', '드라마'), ('PERFORMING ARTS', '공연예술'), ('FAMILY & RELATIONSHIPS', '가족 / 관계'), ('GAMES & ACTIVITIES', '게임 / 활동'), ('FICTION', '소설'), ('HEALTH & FITNESS', '건강 피트니스'), ('HISTORY', '역사'), ('TRUE CRIME', '범죄'), ('GARDENING', '원예'), ('HOUSE & HOME', '가정 / 살림'), ('HUMOR', '유머'), ('LAW', '법'), ('MUSIC', '음악'), ('BODY, MIND & SPIRIT', '몸, 마음, 정신'), ('SELF-HELP', '자기계발'), ('PETS', '애완동물'), ('POETRY', '시'), ('REFERENCE', '참조문헌'), ('BIBLES', '성경'), ('RELIGION', '종교'), ('MEDICAL', '의학'), ('SCIENCE', '과학'), ('PHILOSOPHY', '철학'), ('SOCIAL SCIENCE', '사회과학'), ('SPORTS & RECREATION', '스포츠'), ('NATURE', '자연과학'), ('TRAVEL', '여행'), ('YOUNG ADULT FICTION', '청장년 문학소설'), ('YOUNG ADULT NONFICTION', '청장년 산문문학')], max_length=64)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
