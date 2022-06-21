from django.db import models
from tabnanny import verbose
# Create your models here.

class Book(models.Model):
    class Meta:
        db_table = "Book"

    report_name = models.CharField(max_length = 200, verbose_name = "독후감 제목", blank = False)
    book_name = models.CharField(max_length = 200, verbose_name = "책 제목", blank = False)
    book_author = models.CharField(max_length = 200, verbose_name = "책 글쓴이", blank = False)
    category = models.CharField(max_length = 200, verbose_name = "책 검색", blank = False)
    content = models.TextField(help_text = "독후감을 적어주세요", verbose_name = "독후감 내용")
    created_at = models.DateTimeField(auto_now_add = True, null = True)

    def __str__(self):
        return self.report_name