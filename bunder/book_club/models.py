from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class BookClub(models.Model):
    class Meta:
        db_table = "book_club"

    owner = models.ForeignKey("user.User", on_delete=models.CASCADE, verbose_name="북클럽장")
    club_name = models.CharField(max_length=50, verbose_name="북클럽명", blank=False)
    image = models.CharField(max_length=100, verbose_name="북 클럽 이미지", blank=False)
    category_tuple = [
        ('문학', '문학'),
        ('경제/경영', '경제/경영'),
        ('자기계발', '자기계발'),
        ('인문', '인문'),
        ('정치/사회', '정치/사회'),
        ('예술', '예술'),
        ('과학', '과학'),
        ('기술/IT', '기술/IT'),
    ]
    category = models.CharField(max_length=64, choices=category_tuple)
    member_total = models.IntegerField(validators=[MinValueValidator(2), MaxValueValidator(30)], default=2)
    member_cnt = models.IntegerField(default=1)
    description = models.TextField(help_text="소모임 소개글을 적어주세요.", verbose_name="소모임 소개", null=True)
    link = models.CharField(max_length=200, verbose_name="줌 링크", blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)


class BookClubMember(models.Model):
    class Meta:
        db_table = "club_member"

    user = models.ForeignKey("user.User", on_delete=models.CASCADE, verbose_name="유저 ID")
    club = models.ForeignKey("book_club.BookClub", on_delete=models.CASCADE, verbose_name="소모임 ID", blank=False)
    type_enum = [
        ('MEMBER', 'MEMBER'),
        ('CANDIDATE', 'CANDIDATE'),
        ('OWNER', 'OWNER'),
        ('INVITE', 'INVITE')
    ]
    type = models.CharField(max_length=20, choices=type_enum)


class BookClubVote(models.Model):
    class Meta:
        db_table = "vote"

    club = models.ForeignKey("book_club.BookClub", on_delete=models.CASCADE, verbose_name="소모임 ID")
    topic = models.CharField(max_length=50, verbose_name="투표 주제", blank=False)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()


class VoteDetail(models.Model):
    class Meta:
        db_table = "vote_detail"

    vote = models.ForeignKey("book_club.BookClubVote", on_delete=models.CASCADE, verbose_name="투표")
    description = models.TextField(help_text="투표 상세 내용을 적어주세요.", verbose_name="투표 상세 내용")
    vote_cnt = models.IntegerField(default=0)


class BookClubBooks(models.Model):
    class Meta:
        db_table = "club_book"

    club = models.ForeignKey("book_club.BookClub", on_delete=models.CASCADE, verbose_name="소모임 ID")
    book_name = models.CharField(max_length=200, verbose_name="책 제목", blank=False)
    book_author = models.CharField(max_length=200, verbose_name="책 글쓴이", blank=False)
    image = models.CharField(max_length=200, verbose_name="책 이미지", blank=True)
