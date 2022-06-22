from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include("user.urls")),
    path('book_report/', include("book_report.urls")),
    path('bookclub/', include("book_club.urls")),
]
