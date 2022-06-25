from django.contrib import admin
from .models import User, ProfileBook

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    fields = ['username', 'password', 'age', 'nickname', 'categories']

admin.site.register(User, UserAdmin)

class ProfileBookAdmin(admin.ModelAdmin):
    fields = ['book.book_name', 'username']

admin.site.register(ProfileBook, ProfileBookAdmin)