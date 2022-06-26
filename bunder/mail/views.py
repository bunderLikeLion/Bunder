from django.shortcuts import render, redirect, get_object_or_404
from .models import Mail
# Create your views here.

def main(request):
    return render(request, "mail/mail.html")

def send_mail(request):
    return render(request, "mail/mail_to.html")

def create(request):
    # newmail = Mail()
    # newmail.user = request.user
    # newmail.receiver = request.POST.get('receiver')
    # newmail.content = request.POST.get('context')
    # newmail.save()
    # return redirect('mail:main')
    return 0