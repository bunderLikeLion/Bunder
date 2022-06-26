from django.shortcuts import render, redirect, get_object_or_404
from .models import Mail
# Create your views here.

def main(request):
    return render(request, "mail/mail.html")

def create(request, id):
    newmail = Mail()
    newmail.user = request.user
    newmail.receiver = request.POST.get('receiver')
    newmail.content = request.POST.get('context')
    newmail.save()
    return redirect('mail:main')