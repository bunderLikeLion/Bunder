from django.urls import path, register_converter
from . import views
from . import converters

app_name = 'book_report'

register_converter(converters.HangulSlugConverter, 'slugConverter')

urlpatterns = [
    path('<int:id>', views.detail_report, name="detail"),
    path('write', views.write_report, name="new"),
    path('create', views.create, name="create"),
    path('update/<int:id>', views.update, name='update'),
    path('edit/<int:id>', views.edit, name="edit"),
    path('delete/<int:id>', views.delete, name="delete"),
    path('main', views.main, name="main"),
    path('category/<slugConverter:category>', views.category_search, name="category_search"),
    path('search', views.search, name="search"),
    path('scrap', views.ScrapRequest.as_view()),
    path('myscrap', views.all_scraps.as_view(), name='all_scrap'),
    path('like/', views.likes, name="likes"),
    path('comment', views.CommentRequest.as_view()),
]
