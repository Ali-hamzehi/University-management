from django.contrib import admin
from .models import *


class UserAdmin(admin.ModelAdmin):
    exclude = ('last_login', 'groups', 'user_permissions', 'date_joined', 'is_staff', 'is_active')


class StudentAdmin(UserAdmin):
    exclude = ('last_login', 'groups', 'user_permissions', 'date_joined', 'is_staff', 'is_active')


class ProfessorAdmin(UserAdmin):
    exclude = ('last_login', 'groups', 'user_permissions', 'date_joined', 'is_staff', 'is_active')


class ITmanagerAdmin(UserAdmin):
    exclude = ('last_login', 'groups', 'user_permissions', 'date_joined', 'is_staff', 'is_active')


class EducationalAssistantAdmin(UserAdmin):
    exclude = ('last_login', 'groups', 'user_permissions', 'date_joined', 'is_staff', 'is_active')


admin.site.register(User, UserAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Professor, ProfessorAdmin)
admin.site.register(ITmanager, ITmanagerAdmin)
admin.site.register(EducationalAssistant, EducationalAssistantAdmin)
