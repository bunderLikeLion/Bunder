from django.urls import path
from . import views

app_name = 'book_report'

urlpatterns = [
    path('main/<int:id>', views.detail_report, name = "detail"),
    path('write_report/', views.write_report, name = "new"),
    path('create/', views.create, name = "create"),
    path('update/<int:id>', views.update, name = 'update'),
    path('edit/<int:id>', views.edit, name = "edit"),
    path('delete/<int:id>', views.delete, name = "delete"),
    path('main/', views.main, name = "main"),
    path('search/', views.search, name = "search"),
]