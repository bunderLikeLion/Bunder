from cmath import log
from contextlib import redirect_stdout
from http.client import HTTPResponse
from django.shortcuts import render, redirect
from django.views import View

from .models import User
from book_club.models import Book
from django.contrib import auth
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.contrib.auth.hashers import check_password
from book_report.models import BookReport
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
        res_data = {'username' : username, 'password' : password, 're_password' : re_password,
                'age' : age, 'categories' : categories, 'nickname' : nickname, 'sex' : sex}

        if not (username and password and re_password and age and categories and nickname):
            res_data["error"] = "입력되지 않은 값이 있습니다"
        elif password != re_password:
            res_data["error"] = "비밀번호가 일치하지 않습니다"
        elif User.objects.filter(nickname=nickname).exists():
            res_data["error"] = "이미 존재하는 닉네임 입니다."
        else:
            user = User.objects.create_user(
                username = username,
                password = password,
                age = age,
                nickname = nickname,
                categories = categories,
                sex = sex,
                avatar = f'https://avatars.dicebear.com/api/{sex}/{nickname}.svg'
            )
            user.save()
            return redirect('user:loginpage')
        return render(request, 'login/sign_up.html', res_data)

#로그인 페이지로 이동
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
            user = auth.authenticate(request, username = username, password = password)
            if user is not None:
                auth.login(request, user)
                return redirect('user:bunder')
            else:
                return render(request, 'login/sign_in.html', {'error' : "아이디 혹은 비밀번호가 다릅니다."})
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
                auth.login(request,user)
                error = {'error' : "비밀번호 변경 성공"}
                return render(request, "user/password_revise.html", error)
            else:
                error = {'error':"새로운 비밀번호를 다시 확인해주세요."}
        else:
            error = {'error':"현재 비밀번호가 일치하지 않습니다."}
    else:
        if not request.user.is_authenticated:
            return HttpResponse("로그인 후 이용해주세요")

    return render(request, "user/password_revise.html", error)

# profile 정보
def profile(request):
    user = request.user
    return render(request, 'user/profile.html', {'user' : user})

# bunder 정보
def bunder(request):
    user = request.user
    my_reports = check_my_two_reports(request)
    return render(request, 'user/bunder.html', {'user' : user, 'my_reports' : my_reports})

# 카테고리 수정
@csrf_exempt
def category_revise(request):
    user = request.user
    if request.method == "POST":
        category = request.POST.get("book_category")
        user.categories = category
        user.save()
        return render(request, "user/category_revise.html", {'user' : user})
    else:
        if not request.user.is_authenticated:
            return HttpResponse("로그인 후 이용해주세요")

# 내 독후감 확인 (all_my_reports)
def search_my_reports(request):
    my_reports = check_my_reports(request)
    return render(request, 'user/all_my_reports.html', {'my_reports' : my_reports})

# 내 독후감 확인하는 함수
def check_my_reports(request):
    my_reports = BookReport.objects.all()
    user = request.user
    if user:
        my_reports = my_reports.filter(user_id = user.id)
    return my_reports

def check_my_two_reports(request):
    my_reports = BookReport.objects.all()
    user = request.user
    if user:
        my_reports = my_reports.filter(user_id = user.id).order_by('created_at')[:2]
    return my_reports

# 개인 번더 책 추가
class Book(View):
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
