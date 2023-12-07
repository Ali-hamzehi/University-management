from django.shortcuts import render
from .serializer import *
from .models import User, Student, Professor, EducationalAssistant, ITmanager
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password
from rest_framework import generics
from .permissions import *
from processes.models import Semester
from django_filters.rest_framework import DjangoFilterBackend
from .tasks import *
import secrets
from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator

from django.utils.http import urlsafe_base64_decode


class AssistantListCreateView(APIView):
    def get(self, request):
        assistant = EducationalAssistant.objects.all()
        serializer = AssistantSerializer(
            assistant, context={'request': request}, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data.copy()
        # Hash the password before saving
        if 'password' in data:
            data['password'] = make_password(data['password'])

        serializer = AssistantSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AssistantDetailView(APIView):
    def get(self, request, pk):
        assistant = EducationalAssistant.objects.get(pk=pk)
        serializer = AssistantSerializer(
            assistant, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        assistant = EducationalAssistant.objects.get(pk=pk)
        data = request.data.copy()
        # Hash the password before saving
        if 'password' in data:
            data['password'] = make_password(data['password'])

        serializer = AssistantSerializer(instance=assistant, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        assistant = EducationalAssistant.objects.get(pk=pk)
        assistant.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class StudentListCreateView(APIView):

    def get(self, request):
        student = Student.objects.all()
        serializer = StudentSerializer(
            student, context={'request': request}, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data.copy()
        if 'password' in data:
            data['password'] = make_password(data['password'])

        serializer = StudentSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentDetailView(APIView):
    def get(self, request, pk):
        student = Student.objects.get(pk=pk)
        serializer = StudentSerializer(
            student, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        student = Student.objects.get(pk=pk)
        data = request.data.copy()

        if 'password' in data:
            data['password'] = make_password(data['password'])

        serializer = StudentSerializer(instance=student, data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        student = Student.objects.get(pk=pk)
        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class StudentListVeiw(generics.ListAPIView):
    """

    only has get-http method:

        give a list of all Professors
        only admin and EducationalAssistant are allowd to use this api

    """
    permission_classes = [IsEducationalAssistant]
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class RetrieveUpdateStudentView(generics.RetrieveUpdateAPIView):
    """
    GET: 
        retrieve one student
        only admin and EducationalAssistant are allowed to use this method    
    ___

    PUT % PATCH :
        update one student by that specific student
        only the student is allowed to use this method  

    """

    def get_permissions(self):
        if self.request.method == 'GET':

            return [IsEducationalAssistant(),]
        elif self.request.method in ['PUT', 'PATCH']:

            return [IsStudent(),]
        return super().get_permissions()

    serializer_class = StudentSerializer

    def get_queryset(self):

        student = Student.objects.filter(pk=self.kwargs['pk'])

        return student


class ProfessorListVeiw(generics.ListAPIView):
    """
    only has get-http method:

        give a list of all Professors
        only admin and EducationalAssistant are allowd to use this api
    """
    permission_classes = [IsEducationalAssistant]
    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer


class RetrieveUpdateProfessorView(generics.RetrieveUpdateAPIView):
    """
     GET : 
        retrieve one Professor

        only admin and EducationalAssistant are allowd to use this method
    ___

    PUT or PATCH : 
        only the professor can update his/her information 
        user_id is excluded


    """

    def get_permissions(self):
        if self.request.method == 'GET':

            return [IsEducationalAssistant()]
        elif self.request.method in ['PUT', 'PATCH']:

            return [IsProfessor()]
        return super().get_permissions()

    serializer_class = ProfessorSerializer

    def get_queryset(self):

        return Professor.objects.filter(pk=self.kwargs['pk'])


class SemesterListView(generics.ListAPIView):
    """
    GET :
        each student and professor can use this api 


    """

    queryset = Semester.objects.all()
    serializer_class = SemesterListSerializer


class RetrieveSemester(generics.RetrieveAPIView):
    """
    GET :
        accept the id of the model
        each student and Professor can observe the details of one Semester

    """

    serializer_class = SemesterSerializer

    def get_queryset(self):
        return Semester.objects.filter(pk=self.kwargs['pk'])


def PickStudent(self):
    pk = self.kwargs["pk"]
    try:
        pk = int(pk)
        return str(pk)
    except:
        return Student.objects.get(user_ptr_id=self.request.user.id).id
class PickableCourses(generics.ListAPIView):
    """
    GET:

        this api renders all the possible courses one student can take this term 


        The Logged in Student call the url like this : 
            student/me/my-courses/
        Admin and EducationalAssistant call the url like this ;
            student/4011136578/my-courses/   
            admin and EducationalAssistant should use student id of students


    """

    def get_permissions(self):

        if self.kwargs["pk"] != "me":
            return [IsEducationalAssistant(),]

        return super().get_permissions()

    serializer_class = PickableCoursesSerializers

    def get_queryset(self):

        student = Student.objects.get(pk=PickStudent(self))

        study_fields = student.study_field.all()

        allCourse = list()

        for study_field in study_fields:
            all_courses = study_field.units.all()
            for unit in all_courses:
                allCourse.append(unit)

        def PickableCourses(Courses, student):
            CoursesList = Courses

            for course in CoursesList:
                prerequisites = course.prerequisites.all()
                for prerequisite in prerequisites:
                    if prerequisite not in student.passed_courses.all():
                        CoursesList.remove(course)
                        break

            for course in Courses:
                if course in student.passed_courses.all():
                    CoursesList.remove(course)

            return CoursesList

        return PickableCourses(allCourse, student)


class PassedCourseStatus(generics.ListAPIView):
    """
    Get:
        this api renders all courses that the student passed 
    """

    def get_permissions(self):

        if self.kwargs["pk"] == "me":
            return [IsStudent]

        elif self.kwargs['pk'] != 'me':
            return [IsEducationalAssistant]

        return super().get_permissions()

    serializer_class = PickableCoursesSerializers

    def get_queryset(self):
        passed_courses = Student.objects.get(
            pk=PickStudent(self)).passed_courses.all()
        return passed_courses


class TermCourseStatus(generics.ListAPIView):
    """
    GET:
        this api renders all the courses that the student is currently studing


    """

    def get_permissions(self):

        if self.kwargs["pk"] == "me":
            return [IsStudent]

        elif self.kwargs['pk'] != 'me':
            return [IsEducationalAssistant]

        return super().get_permissions()

    serializer_class = PickableCoursesSerializers

    def get_queryset(self):
        in_progress_courses = Student.objects.get(
            pk=PickStudent(self)).in_progress_courses.all()
        return in_progress_courses


class RemainingSanavat(generics.RetrieveAPIView):
    """
    GET:
        this api renders  how many years is left to end of the educational journy 

    """

    def get_permissions(self):

        if self.kwargs["pk"] == "me":
            return [IsStudent]

        elif self.kwargs['pk'] != 'me':
            return [IsEducationalAssistant]

        return super().get_permissions()

    serializer_class = SanavatSerializers

    def get_object(self):
        sanavat = Student.objects.get(pk=PickStudent(self)).sanavat
        return {"sanavat": sanavat}


class CreateGetProfessor(generics.ListCreateAPIView):
    """
    GET:
        only Itmanager can get a list of all professors

        ____
    POST:
        only ITmanager can create professor
    """
    permission_classes = [IsITmanager]
    queryset = Professor.objects.all()
    serializer_class = CreateProfessorSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['firstname', 'lastname', 'user_id',
                        'national_id', 'college', 'rank',
                        'field']


class RetrieveUpdateDestroyprofessor(generics.RetrieveUpdateDestroyAPIView):
    """
    GET PUT PATCH DELETE:
        only Itmanager can call these methods

    """
    permission_classes = [IsITmanager]
    serializer_class = CreateProfessorSerializer

    def get_queryset(self):

        professor_id = self.kwargs.get('pk')
        return Professor.objects.filter(pk=professor_id)


def generate_password_change_token(user):
    return secrets.token_urlsafe(32)


class ChangePasswordRequest(generics.GenericAPIView):
    def post(self,request):
        user = request.user
        email = user.email
        token = generate_password_change_token(user)
        Send_change_password_email.delay(email,token)
        return Response({'message': 'Password change request received'})
    


class ChangePasswordAction(generics.GenericAPIView):
    def post(self,request,token):
        try:
            uid = str(urlsafe_base64_decode(token))
        except Exception as e:
            print(e)
            return Response({'error': 'Invalid token'}, status=400)

        user = get_object_or_404(User, pk=uid)
 
        if default_token_generator.check_token(user, token):
            serializer = ChangePasswordSerializer(request.data)
            serializer.is_valid(raise_exception=True)
            new_password = request.data.get('new_password')
            user.set_password(new_password)
            user.save()
            return Response({'message': 'Password changed successfully'})
 
        return Response({'error': 'Invalid token'}, status=400)
        
       
class SudentSemesterCourseShedule(APIView):
    permission_classes = [IsStudent, ]

    def get(self,request,pk):
        student = get_object_or_404(Student, pk=pk)
        student_course_schedule = student.in_progress_courses.all().values('approved_course.course_name', 'class_day_and_time')
        serializer = CourseScheduleSerializer(student_course_schedule , many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
class SudentSemesterCourseExams(APIView):
    permission_classes = [IsStudent, ]
    
    def get(self,request,pk):
        student = get_object_or_404(Student, pk=pk)
        student_course_schedule_exam = student.in_progress_courses.all().values('exam_date_and_time', 'exam_location')
        serializer = CourseExamSerializer(student_course_schedule_exam,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

