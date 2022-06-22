from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import mimetypes

mimetypes.add_type("application/javascript", ".js", True)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include("user.urls")),
    path('book_report/', include("book_report.urls")),
    path('bookclub/', include("book_club.urls")),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
