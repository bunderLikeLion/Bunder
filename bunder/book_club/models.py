from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class BookClub(models.Model):
    class Meta:
        db_table = "book_club"

    owner = models.ForeignKey("user.User", on_delete=models.CASCADE, verbose_name= "북클럽장")
    club_name = models.CharField(max_length = 200, verbose_name = "북클럽명", blank = False)
    image = models.CharField(max_length = 200, verbose_name = "북 클럽 이미지", blank = False)
    category_tuple = [
        ('문학','문학'),
        ('경제/경영','경제/경영'),
        ('자기계발', '자기계발'),
        ('인문', '인문'),
        ('정치/사회', '정치/사회'),
        ('예술', '예술'),
        ('과학', '과학'),
        ('기술/IT', '기술/IT'),
    ]
    category = models.CharField(max_length = 64, choices = category_tuple)
    member_cnt = models.IntegerField(validators=[MinValueValidator(2), MaxValueValidator(30)])
    link = models.CharField(max_length = 200, verbose_name = "줌 링크", blank = False)
    created_at = models.DateTimeField(auto_now_add = True, null = True)
