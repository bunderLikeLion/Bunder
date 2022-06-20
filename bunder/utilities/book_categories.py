# https://blog.lulu.com/bisac-what-it-is-and-why-it-matters/
# 독서 카테고리 해석 입니다. 직접 해석한거라 오역이 있을 수 있으니 수정해 주셔도 됩니다!
# 수정 시 다른 파일에도 수정이 필요하므로 언제 마지막 수정했는지 적어주시면 감사하겠습니다.
# 마지막 수정 : 06.20 03:53 by 금장

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

# 문학 --> 엔틱수집서적 청소년 문학소설 청소년 산문문학 만화/그래픽노블 문학선집 문학비판 드라마 소설 시 청장년 문학소설 청장년 산문문학
# 경제/경영 --> 경제/경영 
# 자기계발 -->  요리 공예/취미 외국어 학습자료 건강 피트니스 원예 게임/활동 몸마음정신 자기계발 여행
# 인문 --> 자서전 교육 언ㅌ어예술 및 규율 가족/관계 역사 가정/살림 유머 애완동물 참조문헌 철학 스포츠
# 정치/사회 --> 범죄 법 성경 종교 사회과학
# 예술 --> 예술 디자인 사진 공연예술 음악
# 과학 --> 수학 의학 과학 자연과학
# 기술/IT --> 컴퓨터 교통 건축 기술/공학