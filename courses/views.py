from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import *
from .models import *
from .permissions import *
from django.utils.translation import gettext as _


class ApprovedCourseListCreateView(APIView):
    permission_classes = [ItManagerOrEducationalAssistant, ]

    def get(self, request):
        message = _("get approved course list")
        version = request.version
        name = request.query_params.get("course_name")
        college = request.query_params.get("provider_college")
        course = ApprovedCourse.objects.all().filter(course_name=name, provider_college=college)
        ser_data = ApprovedCourseSerializer(course, many=True)
        data = {'ser_data': ser_data, 'message': message}
        return Response(data, status.HTTP_200_OK)

    def post(self, request):
        message = _("post approved course")
        version = request.version
        ser_data = ApprovedCourseSerializer(data=request.data)
        if ser_data.is_valid():
            ser_data.save()
            data = {'ser_data': ser_data, 'message': message}
            return Response(data, status=status.HTTP_200_OK)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class ApprovedCoursesDetailView(APIView):
    permission_classes = [ItManagerOrEducationalAssistant, ]

    def get(self, request, pk):
        message = _("get approved course detail")
        version = request.version
        course = ApprovedCourse.objects.get(approved_course_id=pk)
        ser_data = ApprovedCourseSerializer(course)
        data = {'ser_data': ser_data, 'message': message}
        return Response(data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        message = _("update approved course detail")
        version = request.version
        course = ApprovedCourse.objects.get(approved_course_id=pk)
        ser_data = ApprovedCourseSerializer(instance=course, data=request.data, partial=True)
        if ser_data.is_valid():
            ser_data.save()
            data = {'ser_data': ser_data, 'message': message}
            return Response(data, status=status.HTTP_200_OK)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        message = _("delete approved course detail")
        version = request.version
        course = ApprovedCourse.objects.get(approved_course_id=pk)
        course.delete()
        return Response({'message': message}, status=status.HTTP_200_OK)


class SemesterCourseListCreateView(APIView):
    permission_classes = [ItManagerOrEducationalAssistant, IsValidTimeForCreate, ]

    def get(self, request):
        message = _("get semester course list")
        version = request.version
        name = request.query_params.get("course_name")
        college = request.query_params.get("provider_college")
        semester = request.query_params.get("current_semester")
        course = SemesterCourse.objects.all().filter(course_name=name, provider_college=college,
                                                     current_semester=semester)
        ser_data = SemesterCourseSerializer(course)
        data = {'ser_data': ser_data, 'message': message}
        return Response(data, status.HTTP_200_OK)

    def post(self, request):
        message = _("post semester course")
        version = request.version
        ser_data = SemesterCourseSerializer(data=request.data)
        data = {'ser_data': ser_data, 'message': message}
        if ser_data.ia_valid():
            ser_data.save()
            return Response(data, status=status.HTTP_200_OK)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class SemesterCourseDetailView(APIView):
    permission_classes = [ItManagerOrEducationalAssistant, ]

    def get(self, request, pk):
        message = _("get semester course detail")
        version = request.version
        course = SemesterCourse.objects.get(semester_course_id=pk)
        ser_data = SemesterCourseSerializer(course)
        data = {'ser_data': ser_data, 'message': message}
        return Response(data, status=status.HTTP_200_OK)

        def put(self, request, pk):
            message = _("update semester course detail")
            version = request.version
            course = SemesterCourse.objects.get(semester_course_id=pk)
            ser_data = SemesterCourseSerializer(instance=course, data=request.data, partial=True)
            data = {'ser_data': ser_data, 'message': message}
            if ser_data.is_valid():
                ser_data.save()
                return Response(data, status=status.HTTP_200_OK)
            return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

        def delete(self, request, pk):
            message = _("delete semester course detail")
            version = request.version
            course = SemesterCourse.objects.get(semester_course_id=pk)
            self.check_object_permissions(request, course)
            course.delete()
            return Response({'message': message}, status=status.HTTP_200_OK)