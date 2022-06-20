from sre_parse import CATEGORIES
from tabnanny import verbose
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    userid = models.CharField(max_length = 32, unique = True, verbose_name = "아이디", blank = False)
    password = models.CharField(max_length = 32, verbose_name = "비밀번호", blank = False)
    nickname = models.CharField(max_length = 32, unique = True, verbose_name = "닉네임", blank = False)
    age = models.IntegerField(verbose_name = "나이", blank = False, default = 0)

    CATEGORIES_OF_BOOKS = [
        ('ANTIQUES & COLLECTIBLES', '엔틱 & 수집서적'),
        ('ART', '예술'),
        ('DESIGN', '디자인'),
        ('PHOTOGRAPHY', '사진'),
        ('BIOGRAPHY & AUTOBIOGRAPHY', '자서전'),
        ('BUSINESS & ECONOMICS', '경제 / 경영'),
        ('JUVENILE FICTION', '청소년 문학소설'),
        ('JUVENILE NONFICTION', '청소년 산문문학'), # 다른 해석이 있을가요,,
        ('COMICS & GRAPHIC NOVELS', '만화 / 그래픽노블'),
        ('COMPUTERS', '컴퓨터'),
        ('TRANSPORTATION', '교통'),
        ('COOKING', '요리'),
        ('CRAFTS & HOBBIES', '공예 / 취미'),
        ('EDUCATION', '교육'),
        ('FOREIGN LANGUAGE STUDY', '외국어'),
        ('LANGUAGE ARTS & DISCIPLINES', '언어예술 및 규율'),
        ('LITERARY COLLECTIONS', '문학선집'),
        ('LITERARY CRITICISM', '문학비판'),
        ('MATHEMATICS', '수학'),
        ('STUDY AIDS', '학습자료'),
        ('ARCHITECTURE', '건축'),
        ('TECHNOLOGY & ENGINEERING', '기술 / 공학'),
        ('DRAMA', '드라마'),
        ('PERFORMING ARTS', '공연예술'),
        ('FAMILY & RELATIONSHIPS', '가족 / 관계'),
        ('GAMES & ACTIVITIES', '게임 / 활동'),
        ('FICTION', '소설'),
        ('HEALTH & FITNESS', '건강 피트니스'),
        ('HISTORY', '역사'),
        ('TRUE CRIME', '범죄'),
        ('GARDENING', '원예'),
        ('HOUSE & HOME', '가정 / 살림'),
        ('HUMOR', '유머'), 
        ('LAW', '법'),
        ('MUSIC', '음악'),
        ('BODY, MIND & SPIRIT', '몸, 마음, 정신'),
        ('SELF-HELP', '자기계발'),
        ('PETS', '애완동물'),
        ('POETRY', '시'),
        ('REFERENCE', '참조문헌'), # 다른 해석,,?
        ('BIBLES', '성경'),
        ('RELIGION', '종교'),
        ('MEDICAL', '의학'),
        ('SCIENCE', '과학'),
        ('PHILOSOPHY', '철학'),
        ('SOCIAL SCIENCE', '사회과학'),
        ('SPORTS & RECREATION', '스포츠'),
        ('NATURE', '자연과학'), # 다른 해석,,?
        ('TRAVEL', '여행'),
        ('YOUNG ADULT FICTION', '청장년 문학소설'),
        ('YOUNG ADULT NONFICTION', '청장년 산문문학'),
    ]
    categories = models.CharField(max_length = 64, choices = CATEGORIES_OF_BOOKS) # 디폴트값 설정은 어떻게 할가요?
    