from tabnanny import verbose
from django.db import models
from django.contrib.auth.models import AbstractUser
from book_report.models import Book

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

class Scrap(models.Model):
    class Meta:
        db_table = "scrap"

    userid = models.ForeignKey(User, on_delete= models.CASCADE)
    bookid = models.ForeignKey(Book, on_delete=models.CASCADE)