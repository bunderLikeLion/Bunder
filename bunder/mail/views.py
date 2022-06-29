from django.shortcuts import render, redirect, get_object_or_404
from .models import Mail
from django.views.decorators.csrf import csrf_exempt
from user.models import User
from django.db.models import Q
from django.http import HttpResponse, JsonResponse


# Create your views here.

def main(request):
    if request.method == 'GET':
        check_i_send_receiver = Mail.objects.filter(user=request.user).values_list('receiver', flat=True)
        check_you_send_receiver = Mail.objects.filter(receiver_id=request.user.id).values_list('user', flat=True)
        check_receiver = check_i_send_receiver.union(check_you_send_receiver, all=True)
        if request.GET.get("id"):
            click_receiver = request.GET.get("id")
            each_content = Mail.objects.filter(Q(user=request.user) | Q(user=click_receiver),
                                               Q(receiver=click_receiver) | Q(receiver=request.user)).order_by(
                '-created_at')
            receiver = User.objects.filter(id__in=[id for id in check_receiver])
            return render(request, "mail/mail.html",
                          {'receiver': receiver, 'each_content': each_content, 'click_receiver': click_receiver})
        else:
            receiver = User.objects.filter(id__in=[id for id in check_receiver])
            return render(request, "mail/mail.html", {'receiver': receiver})


def send_mail(request):
    return render(request, "mail/mail_to.html")


def reply(request):
    try:
        id = request.GET.get("id")
        receiver = get_object_or_404(User, pk=id)
        return render(request, "mail/mail_to.html", {'receiver': receiver})
    except ValueError:
        check_i_send_receiver = Mail.objects.filter(user=request.user).values_list('receiver', flat=True)
        check_you_send_receiver = Mail.objects.filter(receiver_id=request.user.id).values_list('user', flat=True)
        check_receiver = check_i_send_receiver.union(check_you_send_receiver, all=True)
        receiver = User.objects.filter(id__in=[id for id in check_receiver])
        return render(request, "mail/mail.html", {'error': '상대방을 먼저 선택 하세요.', 'receiver': receiver})


@csrf_exempt
def create(request):
    if request.method == "POST":
        newmail = Mail()
        newmail.user = request.user
        receiver = request.POST.get('receiver')
        newmail.content = request.POST.get('content')
        res_data = {}
        if newmail.content == '':
            res_data['error'] = '내용을 입력해 주세요.'
            return render(request, 'mail/mail_to.html', res_data)
        else:
            try:
                userob = User.objects.get(nickname=receiver)
                newmail.receiver = userob
                newmail.save()
            except User.DoesNotExist:
                res_data['error'] = '존재하지 않는 닉네임 입니다.'
                return render(request, 'mail/mail_to.html', res_data)
        return redirect("/mail/receiver?id=" + str(newmail.receiver.id))
