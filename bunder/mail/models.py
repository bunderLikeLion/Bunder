from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


# Create your models here.

class Mail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    content = models.CharField(max_length=1000)
