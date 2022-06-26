from django.shortcuts import render, redirect, get_object_or_404
from .models import Mail
from django.views.decorators.csrf import csrf_exempt
from user.models import User
from django.http import HttpResponse


# Create your views here.

def main(request):
    return render(request, "mail/mail.html")


def send_mail(request):
    return render(request, "mail/mail_to.html")


@csrf_exempt
def create(request):
    newmail = Mail()
    newmail.user = request.user
    receiver = request.POST.get('receiver')
    newmail.content = request.POST.get('content')
    try:
        userob = User.objects.get(nickname= receiver)
        newmail.receiver = userob
        newmail.save()
    except User.DoesNotExist:
        return HttpResponse("닉네임 없음")
    return redirect('mail:main')
