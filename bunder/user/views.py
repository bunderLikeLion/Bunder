from cmath import log
from http.client import HTTPResponse
from django.shortcuts import render, redirect
from .models import User
from django.contrib import auth
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.contrib.auth.hashers import check_password
import requests

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
        book_category = request.POST["book_category"]
        nickname = request.POST["nickname"]

        res_data = {}

        if not (username and password and re_password and age and book_category and nickname):
            res_data["error"] = "입력되지 않은 값이 있습니다"
        elif password != re_password:
            res_data["error"] = "비밀번호가 일치하지 않습니다"
        else:
            user = User.objects.create_user(
                username = username,
                password = password,
                age = age,
                nickname = nickname,
                categories = book_category,
            )
            user.save()
            return render(request, 'login/sign_up.html', res_data)
    return render(request, 'login/sign_up.html', res_data)

# 로그인
@csrf_exempt 
def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = auth.authenticate(request, username = username, password = password)
        if user is not None:
            auth.login(request, user)
            return render(request, 'login/sign_in.html', {'error' : '로그인 성공'})
        else:
            return render(request, 'login/sign_in.html', {'error' : "아이디 혹은 비밀번호가 다릅니다."})
    else:
        return render(request, 'login/sign_in.html')

# 로그아웃
def logout(request):
    auth.logout(request)
    return HttpResponse("로그아웃")

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
        return render(request, "user/category_revise.html", {'user' : user})