from django.shortcuts import render, redirect
from .models import User
from django.contrib import auth
from django.views.decorators.csrf import csrf_exempt
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
        book_taste = request.POST["book_taste"]
        nickname = request.POST["nickname"]

        res_data = {}

        if not (username and password and re_password and age and book_taste and nickname):
            res_data["error"] = "입력되지 않은 값이 있습니다"
        elif password != re_password:
            res_data["error"] = "비밀번호가 일치하지 않습니다"
        else:
            user = User.objects.create_user(
                username = username,
                password = password,
                age = age,
                nickname = nickname,
                categories = book_taste,
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