from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('signup', views.register, name = 'register'),
    path('login', views.login),
    path('logout', views.logout, name = 'logout'),
    path('profile', views.profile, name="profile"),
    path('updatepassword', views.password_revise),
    path('updateprofile', views.profile_revise),
    path('report', views.reports, name="reports"),
    path('myscrap', views.search_my_scraps, name="search_my_scraps"),
    path('bunder', views.bunder, name="bunder"),
    path('login', views.loginpage, name="loginpage"),
    path('book', views.UserBook.as_view(), name="book"),
    path('profilebook/<int:id>', views.profilebook, name="profilebook"),
    path('bookdetail/<int:id>', views.bookdetail, name="bookdetail"),
    path('del_profilebook/<int:id>', views.del_profilebook, name="del_profilebook"),
    path('club', views.get_book_club_json, name='get_book_club_json'),
]
