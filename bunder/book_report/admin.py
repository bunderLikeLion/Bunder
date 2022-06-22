from django.contrib import admin
from .models import BookReport
# Register your models here.


# Register your models here.
class BookAdmin(admin.ModelAdmin):
    fields = ['user', 'report_name', 'book_name', 'category', 'content']

admin.site.register(BookReport, BookAdmin)