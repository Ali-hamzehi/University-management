from rest_framework.permissions import BasePermission, SAFE_METHODS
from users.models import *
import jdatetime


class IsValidTimeForCreate(BasePermission):

    def has_object_permission(self, request, view, obj):
        today = jdatetime.today()
        restoration_start = obj.current_semester.restoration_end_time
        semester_end = obj.current_semester.semester_end_time
        if restoration_start <= today <= semester_end:
            return False
        return True


class ItManagerOrEducationalAssistant(BasePermission):
    message = 'Access denied'

    def has_permission(self, request, view):
        if request.user.is_authenticated and (request.user.kind == 'I' or request.user.kind == 'E'):
            return True
        return False
