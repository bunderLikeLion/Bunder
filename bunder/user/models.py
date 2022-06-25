from tabnanny import verbose
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    password = models.CharField(max_length = 32, verbose_name = "비밀번호", blank = False)
    nickname = models.CharField(max_length = 32, verbose_name = "닉네임", unique= True, blank = False)
    age = models.IntegerField(verbose_name = "나이", blank = False, default = 0)
    new_category_tuple = [
        ('문학','문학'),
        ('경제/경영','경제/경영'),
        ('자기계발', '자기계발'),
        ('인문', '인문'),
        ('정치/사회', '정치/사회'),
        ('예술', '예술'),
        ('과학', '과학'),
        ('기술/IT', '기술/IT'),
    ]
    categories = models.CharField(max_length = 64, choices = new_category_tuple)
    avatar = models.CharField(max_length=50, verbose_name = "유저 프로필", blank = False)
    sex_tuple = [
        ('mail','mail'),
        ('femail','femail'),
    ]
    sex = models.CharField(max_length=10, choices = sex_tuple, verbose_name = "유저 프로필", blank = False)

class ProfileBook(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    book = models.ForeignKey('book_club.Book', on_delete = models.CASCADE)