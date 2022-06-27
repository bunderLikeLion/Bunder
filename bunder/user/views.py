from django.shortcuts import get_object_or_404, render, redirect
from django.views import View

from .models import ProfileBook, User
from book_club.models import Book, BookClubMember
from django.contrib import auth
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.contrib.auth.hashers import check_password
from book_report.models import BookReport, Scrap
from django.db.models import Q
import json
import os


# Create your views here.

# 회원가입
@csrf_exempt
def register(request):
    if request.method == "GET":
        return render(request, 'login/sign_up.html')
    elif request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        re_password = request.POST["re_password"]
        age = request.POST["age"]
        categories = request.POST["book_category"]
        nickname = request.POST["nickname"]
        sex = request.POST["sex"]
        res_data = {'username': username, 'password': password, 're_password': re_password,
                    'age': age, 'categories': categories, 'nickname': nickname, 'sex': sex}

        if not (username and password and re_password and age and categories and nickname):
            res_data["error"] = "입력되지 않은 값이 있습니다"
        elif password != re_password:
            res_data["error"] = "비밀번호가 일치하지 않습니다"
        elif User.objects.filter(nickname=nickname).exists():
            res_data["error"] = "이미 존재하는 닉네임 입니다."
        elif User.objects.filter(username=username).exists():
            res_data["error"] = "이미 존재하는 아이디 입니다."
        elif len(nickname) > 8:
            res_data["error"] = "닉네임 길이는 최대 8자 입니다."
        elif len(username) > 20:
            res_data["error"] = "아이디 길이는 최대 20자 입니다."
        else:
            user = User.objects.create_user(
                username=username,
                password=password,
                age=age,
                nickname=nickname,
                categories=categories,
                sex=sex,
                avatar=f'https://avatars.dicebear.com/api/{sex}/{nickname}.svg'
            )
            user.save()
            return redirect('user:loginpage')
        return render(request, 'login/sign_up.html', res_data)


# 로그인 페이지로 이동
@csrf_exempt
def loginpage(request):
    return render(request, "login/sign_in.html")


# 로그인
@csrf_exempt
def login(request):
    if request.method == "POST":
        if 'login' in request.POST:
            username = request.POST["username"]
            password = request.POST["password"]
            user = auth.authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('user:bunder')
            else:
                return render(request, 'login/sign_in.html', {'error': "아이디 혹은 비밀번호가 다릅니다."})
        elif 'forgotpassword' in request.POST:
            pass
    else:
        return render(request, 'login/sign_in.html')


# 로그아웃
def logout(request):
    auth.logout(request)
    return redirect('main:home')


# 비밀번호 수정
@csrf_exempt
def password_revise(request):
    error = {}
    if request.method == "POST":
        current_password = request.POST.get("old_password")
        user = request.user
        if check_password(current_password, user.password):
            new_password = request.POST.get("new_password1")
            password_confirm = request.POST.get("new_password2")
            if new_password == password_confirm:
                user.set_password(new_password)
                user.save()
                auth.login(request, user)
                error = {'error': "비밀번호 변경 성공"}
                return render(request, "user/password_revise.html", error)
            else:
                error = {'error': "새로운 비밀번호를 다시 확인해주세요."}
        else:
            error = {'error': "현재 비밀번호가 일치하지 않습니다."}
    else:
        if not request.user.is_authenticated:
            return HttpResponse("로그인 후 이용해주세요")

    return render(request, "user/password_revise.html", error)


# profile 정보
def profile(request):
    user = request.user
    return render(request, 'user/profile.html', {'user': user})


# bunder 정보 - 모든 책, 최근 독후감 2개, 최근 스크랩 2개, 프로필 북, 북클럽
def bunder(request):
    if request.method == 'GET':
        user_info = None
        try:
            user_id = request.GET.get('id')
            user_info = get_object_or_404(User, pk=user_id)
        except:
            user_info = request.user


        book = Book.objects.filter(user_id=user_info.id)
        my_recent_reports = check_two_reports(user_info)
        scrap = check_two_scraps(user_info)
        book_club = getBookClub(user_info)
        mainbook = ProfileBook.objects.filter(user_id=user_info.id).last()
        return render(request, 'user/bunder.html', {'user_info': user_info, 'my_recent_reports': my_recent_reports,
                                                    'scrap': scrap, 'book': book,
                                                    'book_club': book_club, 'mainbook': mainbook})


# 프로필 수정
@csrf_exempt
def profile_revise(request):
    user = request.user
    res_data = {'user' : user}
    if request.method == "POST":
        nickname = request.POST.get('nickname')
        if user.nickname != nickname:
            if User.objects.filter(nickname=nickname).exists():
                res_data["error"] = "이미 존재하는 닉네임 입니다."
                return render(request, "user/profile_revise.html", res_data)
            else:
                user.nickname = request.POST.get('nickname')
                user.age = request.POST.get('age')
                user.categories = request.POST.get('book_category')
                user.save()
                return redirect('user:profile')
        else:
            user.age = request.POST.get('age')
            user.categories = request.POST.get('book_category')
            user.save()
            return redirect('user:profile')
    else:
        return render(request, "user/profile_revise.html", res_data)


# 독후감 확인 (reports)
def reports(request):
    if request.method == "GET":
        userId = request.GET.get("id")
        user_info = get_object_or_404(User, pk=userId)
        user_reports = get_reports(user_info)
        return render(request, 'user/all_user_reports.html', {'user_reports': user_reports, 'user_info': user_info })


# 내 독후감 확인하는 함수2
def get_reports(user):
    my_reports = BookReport.objects.filter(user=user)

    return my_reports


# 내 스크랩 확인 (all_my_scraps)
def search_my_scraps(request):
    my_scraps = check_my_scraps(request)
    return render(request, 'user/all_my_scraps.html', {'my_scraps': my_scraps})


# 내 스크랩 확인하는 함수
def check_my_scraps(request):
    my_scraps = Scrap.objects.all()
    user = request.user
    if user:
        my_scraps = my_scraps.filter(user_id=user.id)
    return my_scraps


# 독후감 최신순 2개 확인 함수
def check_two_reports(user):
    my_reports = BookReport.objects.filter(user=user).order_by('-id')[:2]

    return my_reports


# scrap 2개 뽑아서 번더 전달
def check_two_scraps(user):
    scrap = Scrap.objects.filter(user=user).order_by('-id')[:2]
    return scrap


# 개인 번더 책 추가
class UserBook(View):
    def get(self, request):
        key = json.dumps(os.environ.get('GOOGLE_BOOK_KEY'))
        return render(request, 'user/add_book.html', {'bookSecret': key})

    @csrf_exempt
    def post(self, request):
        book = Book()
        book.user = request.user
        book.book_name = request.POST.get('book_name')
        book.book_author = request.POST.get('book_author')
        book.book_img = request.POST.get('book_img')
        book.category = request.POST.get('book_category')

        book.save()

        return redirect('user:bunder')


# 프로필 책 등록
def profilebook(request, id):
    user = request.user
    book = get_object_or_404(Book, pk=id)
    try:
        mainbook = ProfileBook.objects.get(user_id=user.id)
        mainbook.book = book
        mainbook.save()
    except ProfileBook.DoesNotExist:
        mainbook = ProfileBook()
        mainbook.user = user
        mainbook.book = book
        mainbook.save()
        return redirect('user:bunder')
    return redirect('user:bunder')


# 프로필 책 삭제
def del_profilebook(request, id):
    user = request.user
    mainbook = ProfileBook.objects.get(user_id=user.id)
    mainbook.delete()
    return redirect('user:bunder')


# 책 디테일페이지로 가기
def bookdetail(request, id):
    book = get_object_or_404(Book, pk=id)
    return render(request, 'user/detail_book.html', {'book': book})


def getBookClub(user):
    query = Q()
    query.add(Q(user_id=user.id), query.AND)
    query.add(Q(type="OWNER") | Q(type="MEMBER"), query.AND)

    book_club_member = BookClubMember.objects.prefetch_related('club').filter(query)
    club_list = [memberclub.club for memberclub in book_club_member]

    return club_list
