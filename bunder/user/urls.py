from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('register/', views.register),
    path('login/', views.login),
    path('logout/', views.logout),
    path('profile/', views.profile),
    path('password_revise/', views.password_revise),
    path('category_revise/', views.category_revise),   
]