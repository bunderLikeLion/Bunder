from django.shortcuts import render, redirect, get_object_or_404
from .models import Mail
# Create your views here.

def main(request):
    return render(request, "mail/mail.html")

def new(request):
    return render(request, "mail/mail_to.html")
