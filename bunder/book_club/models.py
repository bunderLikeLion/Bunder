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
        ('자기계발', '자기계발'),
        ('인문', '인문'),
        ('정치/사회', '정치/사회'),
        ('예술', '예술'),
        ('과학', '과학'),
        ('기술/IT', '기술/IT'),
        ('자율', '자율')
    ]
    category = models.CharField(max_length=64, choices=category_tuple)
    member_total = models.IntegerField(validators=[MinValueValidator(2), MaxValueValidator(30)], default=2)
    member_cnt = models.IntegerField(default=1)
    description = models.TextField(help_text="소모임 소개글을 적어주세요.", verbose_name="소모임 소개", null=True)
    zoom_link = models.CharField(max_length=200, verbose_name="줌 링크", blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    kakao_link = models.CharField(max_length=200, verbose_name="카카오톡 링크", blank=True)
    view = models.IntegerField(default=0)
    score = models.IntegerField(default=0)

    def add_member_cnt(self):
        self.member_cnt += 1

    def decrement_member_cnt(self):
        self.member_cnt -= 1


class BookClubMember(models.Model):
    class Meta:
        db_table = "club_member"

    user = models.ForeignKey("user.User", on_delete=models.CASCADE, verbose_name="유저 ID")
    club = models.ForeignKey("book_club.BookClub", on_delete=models.CASCADE, verbose_name="소모임 ID", blank=False)
    type_enum = [
        ('MEMBER', 'MEMBER'),
        ('CANDIDATE', 'CANDIDATE'),
        ('OWNER', 'OWNER'),
        ('INVITE', 'INVITE'),
        ('REJECT', 'REJECT'),
    ]
    type = models.CharField(max_length=20, choices=type_enum, default=type_enum[1][0])

    def get_club_cnt(self):
        return self.club.member_total, self.club.member_cnt



class BookClubVote(models.Model):
    class Meta:
        db_table = "vote"

    club = models.ForeignKey("book_club.BookClub", on_delete=models.CASCADE, verbose_name="소모임 ID")
    topic = models.CharField(max_length=50, verbose_name="투표 주제", blank=False)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)



class VoteDetail(models.Model):
    class Meta:
        db_table = "vote_detail"

    vote = models.ForeignKey("book_club.BookClubVote", on_delete=models.CASCADE, verbose_name="투표")
    description = models.TextField(help_text="투표 상세 내용을 적어주세요.", verbose_name="투표 상세 내용")
    vote_cnt = models.IntegerField(default=0)


class Book(models.Model):
    class Meta:
        db_table = "book"

    club = models.ForeignKey("book_club.BookClub", on_delete=models.CASCADE, verbose_name="소모임 ID", null=True)
    user = models.ForeignKey("user.User", on_delete=models.CASCADE, verbose_name="유저 ID", null=True)
    book_name = models.CharField(max_length=200, verbose_name="책 제목", blank=False)
    book_author = models.CharField(max_length=200, verbose_name="책 글쓴이", blank=False)
    book_img = models.CharField(max_length=200, verbose_name="책 이미지", blank=True)
    category_tuple = [
        ('문학', '문학'),
        ('경제/경영', '경제/경영'),
        ('자기계발', '자기계발'),
        ('인문', '인문'),
        ('정치/사회', '정치/사회'),
        ('예술', '예술'),
        ('과학', '과학'),
        ('기술/IT', '기술/IT'),
        ('기타', '기타')
    ]
    category = models.CharField(max_length=64, choices=category_tuple)
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)


