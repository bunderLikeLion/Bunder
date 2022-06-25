from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('signup', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('profile', views.profile),
    path('updatepassword', views.password_revise),
    path('updatecategory', views.category_revise),
    path('myreport', views.search_my_reports, name = "search_my_reports"),
    path('bunder', views.bunder, name = "bunder"),
    path('login', views.loginpage, name = "loginpage"),
    path('book', views.UserBook.as_view(), name="book"),
    path('profilebook', views.profilebook, name="profilebook"),
    path('bookdetail/<int:id>', views.bookdetail, name="bookdetail"),
]