from django.db import models
from tabnanny import verbose
# Create your models here.

class Book(models.Model):
    class Meta:
        db_title = "Book"

    report_title = models.CharField(max_length = 200, verbose_name = "독후감 제목", blank = False)
    book_search = models.CharField(max_length = 200, verbose_name = "책 검색")
    book_title = models.CharField(max_length = 200, verbose_name = "책 제목", blank = False)
    book_writer = models.CharField(max_length = 200, verbose_name = "책 글쓴이", blank = False)
    category = models.CharField(max_length = 200, verbose_name = "책 검색", blank = False)
    content = models.TextField(help_text = "독후감을 적어주세요", verbose_name = "독후감 내용")