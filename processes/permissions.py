from rest_framework.permissions import BasePermission, SAFE_METHODS
from users.models import *
import jdatetime


class IsItManagerOrReadOnly(BasePermission):
    message = 'access denied'

    def has_permission(self, request, view):
        it_managers = ITmanager.objects.all()
        if request.user in it_managers:
            return True
        return False


class IsStudentOrReadOnly(BasePermission):
    message = 'access denied'

    def has_permission(self, request, view):
        student = Student.objects.all()
        return request.user in student

    def has_object_permission(self, request, view, obj):
        return request.user == obj.applicant_student


class IsAllowToUnitSelection(BasePermission):
    message = 'access denied'

    def has_permission(self, request, view):
        student = Student.objects.all()
        return request.user in student

    def has_object_permission(self, request, view, obj):
        return request.user == obj.student


class IsValidTimeForUnitSelection(BasePermission):
    def has_object_permission(self, request, view, obj):
        today = jdatetime.today()
        unit_selection_start = obj.semester.unit_selection_start_time
        unit_selection_end = obj.semester.unit_selection_end_time
        if unit_selection_start <= today <= unit_selection_end:
            return True
        return False


class IsStudentorEducationalAssistant(BasePermission):
    message = 'you are not Student or EducationalAssistant'

    def has_permission(self, request, view):
        if Student.objects.get(user_ptr_id=request.user.id) or EducationalAssistant.objects.get(
                user_ptr_id=request.user.id):
            return True

        return False


class SemesterTimeCheckPermission(BasePermission):
    message = 'You are not allowed to select units at this time'

    def has_permission(self, request, view):

        pk = view.kwargs.get('pk')
        student = Student.objects.get(pk=pk)

        semester_instance = student.current_semester
        if semester_instance:

            start_time = semester_instance.unit_selection_start_time.togregorian()
            end_time = semester_instance.unit_selection_end_time.togregorian()
            current_time = jdatetime.datetime.now()

            if start_time <= current_time and current_time <= end_time:
                return True

        return False


class IsEducationalAssistant(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_educational_assistant


class IsStudentorEducationalAssistant(BasePermission):
    message = 'You need to be the student or EA'

    def has_permission(self, request, view):
        if Student.objects.get(user_ptr_id=request.user.id) or EducationalAssistant.objects.get(
                user_ptr_id=request.user.id):
            return True

        return False


class SemesterResorasionTimeCheckPermission(BasePermission):
    message = 'You are not allowed to select units at this time'

    def has_permission(self, request, view):

        pk = view.kwargs.get('pk')
        student = Student.objects.get(pk=pk)

        semester_instance = student.current_semester
        if semester_instance:

            start_time = semester_instance.restoration_start_time.togregorian()
            end_time = semester_instance.restoration_end_time.togregorian()
            current_time = jdatetime.datetime.now()

            if start_time <= current_time and current_time <= end_time:
                return True

        return False
