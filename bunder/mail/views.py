from django.shortcuts import render, redirect, get_object_or_404
from .models import Mail
from django.views.decorators.csrf import csrf_exempt
from user.models import User
from django.http import HttpResponse, JsonResponse


# Create your views here.

def main(request):
    if request.method == 'GET':
        if request.GET.get("receiver"):
            return HttpResponse("이미 멤버로 추가된 유저입니다.")

        else:
            check_receiver = Mail.objects.filter(user=request.user).values_list('receiver', flat=True).distinct()
            receiver = User.objects.filter(id__in=[id for id in check_receiver])
            each_mail = request.GET.get('each_mail')
            return render(request, "mail/mail.html", {'receiver': receiver})


def send_mail(request):
    return render(request, "mail/mail_to.html")


@csrf_exempt
def create(request):
    newmail = Mail()
    newmail.user = request.user
    receiver = request.POST.get('receiver')
    newmail.content = request.POST.get('content')
    res_data = {}
    try:
        userob = User.objects.get(nickname= receiver)
        newmail.receiver = userob
        newmail.save()
    except User.DoesNotExist:
        res_data['error'] = '존재하지 않는 닉네임 입니다.'
        return render(request, 'mail/mail_to.html', res_data)
    return redirect('mail:main')