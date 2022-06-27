from django.urls import path
from . import views

app_name = 'mail'

urlpatterns = [
    path('receiver', views.main, name='main'),
    path('new', views.send_mail, name="send_mail"),
    path('create', views.create, name="create"),
    ]