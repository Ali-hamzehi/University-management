from rest_framework import permissions
from users.models import *


class IsEducationalAssistant(permissions.BasePermission):

    def has_permission(self, request, view):

        if request.user.username == "admin" or EducationalAssistant.objects.get(
                user_ptr_id=request.user.id):
            return True
        return False


class IsProfessor(permissions.BasePermission):
    def has_permission(self, request, view):

        if request.user.username == "admin" or Professor.objects.get(
                user_ptr_id=request.user.id):
            return True
        return False


class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        if Student.objects.get(
                user_ptr_id=request.user.id):
            return True
        return False


class StudentHasPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.id == obj.id:
            return True
        return False


class IsITmanager(permissions.BasePermission):
    def has_permission(self, request, view):
        if ITmanager.objects.get(
                user_ptr_id=request.user.id):
            return True
        return False
