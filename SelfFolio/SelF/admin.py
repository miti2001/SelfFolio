from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Profile, Attendance, Expense, Grade

# Register your models here.

admin.site.register(Profile)
admin.site.register(Attendance)
admin.site.register(Expense)
admin.site.register(Grade)