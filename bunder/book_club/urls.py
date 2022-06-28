from django.urls import path
from . import views

app_name = 'book_club'

urlpatterns = [
    path('new/', views.new, name="new"),
    path('<int:bookclub_id>', views.book_club_detail, name='book_club_detail'),
    path('vote', views.VoteRequest.as_view()),
    path('vote/list', views.Vote.as_view()),
    path('book', views.ClubBook.as_view(), name='book'),
    path('admit', views.club_admit.as_view()),
    path('', views.main, name='main'),
    path('list', views.book_club_list, name="book_club_list"),
    path('edit/<int:bookclub_id>', views.book_club_edit, name="book_club_edit"),
    path('cover', views.get_book_club_image, name='get_book_club_image'),
    path('myclub', views.get_my_book_club_json, name='get_my_book_club_json'),

    # 소모임 멤버 관련 url
    path('member/', views.request_member, name='request_member'),
    path('reject', views.member_reject.as_view()),
    path('accept', views.response_accept, name='response_invite'),
    path('invite', views.Invite.as_view()),

    # 화상 채팅 관련 url
    path('room/<int:bookclub_id>', views.room),
    path('get_token/', views.getToken),
    path('create_member/', views.createMember),
    path('get_member/', views.getMember),
    path('delete_member/', views.deleteMember),
]