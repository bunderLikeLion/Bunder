from django.shortcuts import render, redirect
from .models import User
from django.contrib import auth
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def register(request):
    return 0

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