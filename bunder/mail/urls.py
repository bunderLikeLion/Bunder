from django.urls import path
from . import views

app_name = 'mail'

urlpatterns = [
    path('', views.main, name='main'),
    path('new', views.create, name="new"),
]
