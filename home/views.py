from django.shortcuts import render, redirect
from django.conf import settings
from django.core.mail import send_mail
import email
import imaplib
from email.header import decode_header


# Create your views here.
def index(request):
    return render(request, 'index.html')


def inbox(request):
    return render(request, 'inbox.html')


def compose(request):
    if request.method == 'POST':
        receiver = [request.POST.get("email")]
        subject = request.POST.get("subject")
        message = request.POST.get("message")
        sender = settings.EMAIL_HOST_USER
        send_mail(subject, message, sender, receiver)
    return render(request, 'compose.html')
