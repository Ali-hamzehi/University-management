from functools import partial
from django.shortcuts import get_object_or_404
from .tasks import *
from courses.models import *
from .models import *
from users.models import *
from .serializer import *
from .permissions import *
from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.settings import api_settings
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from django.http import Http404


# Create your views here.


class StudentListCreateAppealRequest(generics.ListCreateAPIView):
    serializer_class = StudentAppealRequestSerializer

    def get_queryset(self):
        student_id = self.kwargs.get('student_pk', None)
        course_pk = self.kwargs.get('course_pk', None)
        return AppealRequest.objects.filter(student=student_id, course=course_pk)


class StudentRetrieveUpdateDestroyAppealRequest(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = StudentAppealRequestSerializer

    def get_queryset(self):
        student_id = self.kwargs.get('student_pk', None)
        course_pk = self.kwargs.get('course_pk', None)
        request_pk = self.kwargs.get('pk', None)
        return AppealRequest.objects.filter(student=student_id, course=course_pk, pk=request_pk)


class ApproveGradesAPIView(generics.UpdateAPIView):
    serializer_class = ApproveGradesSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        professor_id = self.kwargs['professor_id']
        course_id = self.kwargs['course_id']
        professor = get_object_or_404(Professor, id=professor_id)
        course = get_object_or_404(SemesterCourse, id=course_id)

        # Check if the professor is assigned to the course
        if course.course_professor != professor:
            return None

        # Check if the course has a pending grade
        student_grade = get_object_or_404(StudentGrade, course=course, is_confirmed=False)

        return student_grade

    def perform_update(self, serializer):
        # Set is_confirmed to True during the update
        serializer.save(is_confirmed=True)


class ApprovedCoursesByProfessorsAPIView(generics.ListAPIView):
    serializer_class = SemesterCourseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        assistant_id = self.kwargs['assistant_id']
        course_id = self.kwargs['pk']

        return SemesterCourse.objects.filter(
            college__educationalassistant__id=assistant_id,
            college__educationalassistant__college__id=course_id,
            is_confirmed=True
        )


class CourseDetailByProfessorApprovalView(generics.RetrieveAPIView):
    serializer_class = SemesterCourseDetailSerializer
    permission_classes = [IsAuthenticated]


def get_object(self):
    assistant_id = self.kwargs['assistant_id']
    course_id = self.kwargs['course_id']
    professor_id = self.kwargs['professor_id']

    assistant = get_object_or_404(EducationalAssistant, id=assistant_id)
    course = get_object_or_404(SemesterCourse, id=course_id, course_professor=professor_id)

    return course if assistant.college == course.college else None


class ProfessorListAppealRequest(generics.ListAPIView):
    serializer_class = ProfessorAppealRequestSerializer

    def get_queryset(self):
        professor_id = self.kwargs.get('professor_id')
        course_pk = self.kwargs.get('course_pk')
        return AppealRequest.objects.filter(course__course_professor__id=professor_id, course__id=course_pk)


class ProfosserRetrieveUpdateDestroyAppealRequest(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProfessorAppealRequestSerializer

    def get_queryset(self):
        professor_id = self.kwargs.get('professor_id', None)
        course_pk = self.kwargs.get('course_pk', None)
        request_pk = self.kwargs.get('pk', None)
        return AppealRequest.objects.filter(course__course_professor__id=professor_id, course=course_pk, pk=request_pk)


class ListCreateStudyingEvidence(generics.ListCreateAPIView):
    serializer_class = StudyingEvidenceSerializer

    def get_queryset(self):
        student_id = self.kwargs.get('student_pk', None)
        return EmploymentInSpecialEducationForBoysRequest.objects.filter(applicant_student=student_id)

    def perform_create(self, serializer):
        serializer.save()


class RetrieveUpdateDestroyStudyingEvidence(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = StudyingEvidenceSerializer

    def get_queryset(self):
        student_pk = self.kwargs.get('student_pk', None)
        studying_evidence_pk = self.kwargs.get('pk', None)
        return EmploymentInSpecialEducationForBoysRequest.objects.filter(applicant_student_id=student_pk,
                                                                         pk=studying_evidence_pk)


class AssistantListStudyingEvidence(generics.ListAPIView):
    serializer_class = StudyingEvidenceSerializer

    def get_queryset(self):
        student_id = self.kwargs.get('student_pk', None)
        return EmploymentInSpecialEducationForBoysRequest.objects.filter(applicant_student=student_id)


class AssistantRetriveUpdateStudingEvidence(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = StudyingEvidenceSerializer

    def get_queryset(self):
        student_pk = self.kwargs.get('student_pk', None)
        studying_evidence_pk = self.kwargs.get('pk', None)
        return EmploymentInSpecialEducationForBoysRequest.objects.filter(applicant_student_id=student_pk,
                                                                         pk=studying_evidence_pk)

    def perform_update(self, serializer):
        instance = serializer.save()
        serializer.is_valid(raise_exception=True)
        if instance.is_approved == "A":
            send_confirmed_email_ForBoysRequest.delay(instance.student.user.email)
        elif instance.is_approved in ["W", "R"]:
            send_reject_email_ForBoysRequest(instance.student.user.email)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# KIA:
class CreateCollegeView(APIView):
    permission_classes = [IsItManagerOrReadOnly, ]

    def post(self, request):
        ser_data = CollegeSerializer(data=request.data)
        if ser_data.is_valid():
            ser_data.save()
            return Response(ser_data.data, status=status.HTTP_200_OK)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class GetCollegeListView(APIView):
    permission_classes = [IsItManagerOrReadOnly, ]

    def get(self, request):
        colleges = College.objects.all()
        ser_data = CollegeSerializer(colleges, many=True)
        return Response(ser_data.data, status=status.HTTP_200_OK)


class GetCollegeDetailView(APIView):
    permission_classes = [IsItManagerOrReadOnly, ]

    def get(self, request, pk):
        colleges = College.objects.get(pk=pk)
        ser_data = CollegeSerializer(colleges, many=True)
        return Response(ser_data.data, status=status.HTTP_200_OK)


class UpdateCollegeView(APIView):
    permission_classes = [IsItManagerOrReadOnly, ]

    def put(self, request, pk):
        college = College.objects.get(pk=pk)
        ser_data = CollegeSerializer(
            instance=college, data=request.data, partial=True)
        if ser_data.is_valid():
            ser_data.save()
            return Response(ser_data.data, status=status.HTTP_200_OK)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteCollegeView(APIView):
    permission_classes = [IsItManagerOrReadOnly, ]

    def delete(self, request, pk):
        college = College.objects.get(pk=pk)
        college.delete()
        return Response({'message': 'college deleted'}, status=status.HTTP_200_OK)


class TermListCreateView(APIView):
    def get(self, request):
        semester = Semester.objects.all()
        serializer = TermSerializer(
            semester, context={'request': request}, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data.copy()

        serializer = TermSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TermDetailView(APIView):
    def get(self, request, pk):
        semester = Semester.objects.get(pk=pk)
        serializer = TermSerializer(
            semester, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        semester = Semester.objects.get(pk=pk)
        data = request.data.copy()

        serializer = TermSerializer(instance=semester, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        semester = Semester.objects.get(pk=pk)
        semester.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class StudentEmergencyRemovalSemesterRequest(APIView):
    permission_classes = [IsStudentOrReadOnly, IsEducationalAssistant, ]

    def get(self, request, pk):
        RemovalSemesters = EmergencyRemovalSemesterRequest.objects.filter(applicant_student__user_number=pk)
        self.check_object_permissions(request, RemovalSemesters)
        if RemovalSemesters.exists():
            serializer = RemovalSemesterRequestSerializer(
                RemovalSemesters, many=True, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response("No requests until now", status=status.HTTP_404_NOT_FOUND)

    def post(self, request, pk):
        try:
            student = Student.objects.get(user_number=pk)
        except Student.DoesNotExist:
            return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = RemovalSemesterRequestSerializer(data=request.data)
        per_data = request.query_params.all()
        self.check_object_permissions(request, per_data)
        if serializer.is_valid():
            serializer.save(applicant_student=student)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        RemovalSemester = EmergencyRemovalSemesterRequest.objects.get(applicant_student__user_number=pk)
        self.check_object_permissions(request, RemovalSemester)
        data = request.data.copy()

        serializer = RemovalSemesterRequestSerializer(
            instance=RemovalSemester, data=data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        
        RemovalSemester = EmergencyRemovalSemesterRequest.objects.get(applicant_student__user_number=pk)
        self.check_object_permissions(request, RemovalSemester)
        RemovalSemester.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AssistantEmergencyRemovalSemesterListView(APIView):
    permission_classes = [IsEducationalAssistant, ]

    def get(self, request, pk):
        RemovalSemesters = EmergencyRemovalSemesterRequest.objects.filter(educational_assistant__user_number=pk)

        if RemovalSemesters.exists():
            serializer = RemovalSemesterRequestSerializer(
                RemovalSemesters, many=True, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response("No requests until now", status=status.HTTP_404_NOT_FOUND)


class AssistantEmergencyRemovalSemesterDetail(APIView):
    permission_classes = [IsEducationalAssistant, ]

    def get(self, request, pk, s_pk):
        RemovalSemesters = EmergencyRemovalSemesterRequest.objects.filter(educational_assistant__user_number=pk,
                                                                      applicant_student__user_number=s_pk)

        if RemovalSemesters.exists():
            serializer = RemovalSemesterRequestSerializer(
                RemovalSemesters, many=True, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response("No requests until now", status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        data = request.data.copy()
        serializer = RemovalSemesterRequestSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            if serializer.data.request_result == 'A':
                send_confirmed_email_removal_request(serializer.data.applicant_student.email)
            elif serializer.data.request_result == 'R':
                send_reject_email_removal_request(serializer.data.applicant_student.email)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentEmergencyCourseRemovalRequestView(APIView):            
    permission_classes=[IsStudentOrReadOnly, IsEducationalAssistant,]
    def get(self, request, pk, c_pk):
        course_request = EmergencyRemovalCourseRequest.objects.filter(applicant_student__user_number=pk,semester_course_id = c_pk)


        self.check_object_permissions(request, course_request)
        if course_request.exists():
            serializer = EmergencyCourseRemovalRequestSerializer(
                course_request, context={'request': request}, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response("No requests until now", status=status.HTTP_404_NOT_FOUND)

    def post(self, request, pk, c_pk):
        try:
            student = Student.objects.get(user_number=pk)
        except Student.DoesNotExist:
            return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = EmergencyCourseRemovalRequestSerializer(data=request.data)
        per_data = request.query_params.all()
        self.check_object_permissions(request, per_data)
        if serializer.is_valid():
            course = SemesterCourse.objects.get(semester_course_id=c_pk)
            serializer.save(applicant_student=student, course=course )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk, c_pk):
        emergency_removal_course = EmergencyRemovalCourseRequest.objects.get(applicant_student__user_number=pk, semester_course_id=c_pk)
        self.check_object_permissions(request, emergency_removal_course)
        data = request.data.copy()
        serializer = EmergencyCourseRemovalRequestSerializer(
            instance=emergency_removal_course , data=data , partial=True, context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,  status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, c_pk):
        emergency_removal_course = EmergencyRemovalCourseRequest.objects.get(applicant_student__user_number=pk, semester_course_id=c_pk)
        self.check_object_permissions(request, emergency_removal_course)
        emergency_removal_course.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class AssistantEmergencyRemoveCourseListView(APIView):
    permission_classes= [IsEducationalAssistant,]
    def get(self, request, pk):
        emergency_removal_course = EmergencyRemovalCourseRequest.objects.filter(educational_assistant__user_number=pk)
        if emergency_removal_course.exists():
            serializer=EmergencyCourseRemovalRequestSerializer(emergency_removal_course, many=True, context={'request': request})

            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response("No requests until now", status=status.HTTP_404_NOT_FOUND)
        

class AssistantEmergencyRemoveCourseDetailView(APIView):
    permission_classes= [IsEducationalAssistant,]
    def get(self, request, pk, s_pk):
        emergency_removal_course = EmergencyRemovalCourseRequest.objects.filter(educational_assistant__user_number=pk, applicant_student__user_number=s_pk)
        # self.check_object_permissions(request, emergency_removal_course)
        if emergency_removal_course.exists():
            serializer = EmergencyCourseRemovalRequestSerializer(
                emergency_removal_course, context={'request': request}, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response("No requests until now", status=status.HTTP_404_NOT_FOUND)

    def post(self, request,pk):
        data = request.data.copy()
        student=Student.objects.get(user_number=pk)
        serializer = EmergencyCourseRemovalRequestSerializer(data=data)
        # self.check_object_permissions(request, serializer.data)

        if serializer.is_valid():
            serializer.save()
            if serializer.data.request_result == 'A':
                in_progress_course=student.objects.get(in_progress_courses_semester_course_id=serializer.data['course_semester_course_id'])
                in_progress_course.delete()
                send_confirmed_email_removal_request(serializer.data.applicant_student.email)

            elif serializer.data.request_result == 'R':
                send_reject_email_removal_request(serializer.data.applicant_student.email)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UnitSelectionCheckView(APIView):
    permission_classes = [IsAllowToUnitSelection, IsValidTimeForUnitSelection]

    def post(self, request,pk):
        try:
            student = Student.objects.get(user_number=pk)
        except Student.DoesNotExist:
            return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)
        
        data = {'student': student.id, 'requested_courses': request.data.get('requested_courses')}
        serializer = UnitSelectionRequestSerializer(data=data)
        per_data = request.query_params.all()
        self.check_object_permissions(request, per_data)


        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UnitSelectionSubmitView(APIView):
    permission_classes = [IsAllowToUnitSelection, IsValidTimeForUnitSelection]

    authentication_classes = []
    def post(self, request ,pk):
        try:
            student = Student.objects.get(user_number=pk)
        except Student.DoesNotExist:
            return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)
        data = {'student': student.id, 'requested_courses': request.data.get('requested_courses')}
        serializer = UnitSelectionRequestSerializer(data=data)
        per_data = request.query_params.all()
        self.check_object_permissions(request, per_data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UnitSelectionSendFormView(APIView):
    permission_classes = [IsAllowToUnitSelection, IsValidTimeForUnitSelection]
    authentication_classes = []
    def post(self, request ,pk):
        try:
            student = Student.objects.get(user_number=pk)
        except Student.DoesNotExist:
            return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)
        data = {'student': student.id, 'requested_courses': request.data.get('requested_courses') , 'is_approved' :request.data.get('is_approved')}
        serializer = UnitSelectionRequestSerializer(data=data)
        per_data = request.query_params.all()
        self.check_object_permissions(request, per_data)

        if serializer.is_valid():
            unit_selection_request = serializer.save()
            if unit_selection_request.is_approved == 'A'  :
                student.in_progress_courses.add(*unit_selection_request.requested_courses.all())
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateUnitSelectionRequestView(generics.GenericAPIView):
    """

    """
    permission_classes = [
        IsStudentorEducationalAssistant, SemesterTimeCheckPermission]

    serializer_class = CreateUnitSelectionSerializer

    def post(self, request, pk):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        student = Student.objects.get(pk=self.GetStudent(pk))
        serializer.validated_data["student"] = student
        serializer.validated_data["is_approved"] = "W"
        serializer.save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}

    def GetStudent(self, pk):
        try:
            pk = int(pk)
            return str(pk)
        except:
            return self.request.user.user_id


class ProfessorStudentsSelectionFormsView(generics.ListAPIView):
    serializer_class = UnitSelectionFormSerializer

    def get_queryset(self):
        professor_id = self.kwargs.get('professor_id', None)

        # Assuming you have a ForeignKey from UnitSelectionRequest to SemesterCourse
        semester_courses_taught_by_professor = SemesterCourse.objects.filter(
            course_professor__id=professor_id)

        # Retrieve students related to the semester courses taught by the professor
        queryset = Student.objects.filter(
            unitselectionrequest__requested_courses__in=semester_courses_taught_by_professor).distinct()
        return queryset


class ProfessorStudentsSelectionFormsDetailView(generics.RetrieveAPIView):
    serializer_class = UnitSelectionRequestFormDetailSerializer

    def get_object(self):
        professor_id = self.kwargs.get('professor_id', None)
        student_id = self.kwargs.get('pk', None)
        semester_courses_taught_by_professor = SemesterCourse.objects.filter(
            course_professor__id=professor_id)
        queryset = UnitSelectionRequest.objects.filter(
            student__id=student_id, requested_courses__in=semester_courses_taught_by_professor).distinct()[0]
        return queryset


class ProfessorStudentsSubstitutionFormsView(generics.ListAPIView):
    serializer_class = RestorationRequestFormSerializer

    def get_queryset(self):
        professor_id = self.kwargs.get('professor_id', None)
        semester_courses_taught_by_professor = SemesterCourse.objects.filter(
            course_professor__id=professor_id)
        queryset = Student.objects.filter(
            Q(restorationrequest__added_courses__in=semester_courses_taught_by_professor) & Q(
                restorationrequest__dropped_courses__in=semester_courses_taught_by_professor)).distinct()
        return queryset


class ProfessorStudentsSubstitutionFormsDetailView(generics.RetrieveAPIView):
    serializer_class = RestorationRequestFormDetailSerializer

    def get_object(self):
        professor_id = self.kwargs.get('professor_id', None)
        student_id = self.kwargs.get('pk', None)
        semester_courses_taught_by_professor = SemesterCourse.objects.filter(
            course_professor__id=professor_id)
        queryset = RestorationRequest.objects.filter(Q(added_courses__in=semester_courses_taught_by_professor) & Q(
            dropped_courses__in=semester_courses_taught_by_professor), student__id=student_id).distinct()[0]
        return queryset


# class SelectionCreateView(generics.CreateAPIView):
#     serializer_class = ProfessorSelectionForm
#     def perform_create(self, serializer):
#         serializer.save()


class SelectionFormApprovalView(generics.UpdateAPIView):
    serializer_class = ProfessorSelectionForm

    def get_queryset(self):
        professor_id = self.kwargs.get('professor_id', None)
        student_id = self.kwargs.get('pk', None)
        semester_courses_taught_by_professor = SemesterCourse.objects.filter(
            course_professor__id=professor_id)
        queryset = RestorationRequest.objects.filter(Q(added_courses__in=semester_courses_taught_by_professor) & Q(
            dropped_courses__in=semester_courses_taught_by_professor), student__id=student_id).distinct()[0]
        return queryset

    def perform_update(self, serializer):
        instance = serializer.save()
        serializer.is_valid(raise_exception=True)
        if instance.is_approved == "A":
            send_approval_email.delay(instance.student.user.email)
        elif instance.is_approved in ["W", "R"]:
            send_rejection_email(instance.student.user.email)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class SubstitutionFormCreateView(generics.CreateAPIView):
#     serializer_class = ProfessorSubstitutionFormSerializer

#     def perform_create(self, serializer):
#         serializer.save()

class SubstitutionFormApprovalView(generics.UpdateAPIView):
    serializer_class = ProfessorSubstitutionFormSerializer

    def get_queryset(self):
        professor_id = self.kwargs.get('professor_id', None)
        student_id = self.kwargs.get('pk', None)
        semester_courses_taught_by_professor = SemesterCourse.objects.filter(
            course_professor__id=professor_id)
        queryset = RestorationRequest.objects.filter(Q(added_courses__in=semester_courses_taught_by_professor) & Q(
            dropped_courses__in=semester_courses_taught_by_professor), student__id=student_id).distinct()[0]
        return queryset

    def perform_update(self, serializer):
        instance = serializer.save()
        serializer.is_valid(raise_exception=True)
        if instance.is_approved == "A":
            send_approval_email.delay(instance.student.user.email)
        elif instance.is_approved in ["W", "R"]:
            send_rejection_email(instance.student.user.email)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateUnitSelectionRequestView(generics.GenericAPIView):
    """

    """
    permission_classes = [
        IsStudentorEducationalAssistant, SemesterTimeCheckPermission]

    serializer_class = CreateUnitSelectionSerializer

    def post(self, request, pk):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        student = Student.objects.get(pk=self.GetStudentId(pk))
        serializer.validated_data["student"] = student
        serializer.validated_data["is_approved"] = "W"
        serializer.save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}

    def GetStudentId(self, pk):
        try:
            pk = int(pk)
            return str(pk)
        except:
            return Student.objects.get(user_ptr_id=self.request.user.id).id


class RetrieveUnitSelectionRequestView(generics.RetrieveAPIView):
    serializer_class = RetrieveUnitSelectionRequestSerializer

    def get_object(self):
        pk = self.kwargs['pk']
        student = Student.objects.get(pk=self.GetStudentId(pk))
        queryset = UnitSelectionRequest.objects.filter(student=student).order_by('-submitted_date')
        return queryset.first()

    def GetStudentId(self, pk):
        try:
            pk = int(pk)
            return str(pk)
        except:
            return Student.objects.get(user_ptr_id=self.request.user.id).id


class CreateRestorationRequestView(generics.CreateAPIView):
    serializer_class = CreateRestorationRequestSerializer
    permission_classes = [
        IsStudentorEducationalAssistant, SemesterResorasionTimeCheckPermission]

    def perform_create(self, serializer):
        pk = self.kwargs["pk"]
        student = Student.objects.get(pk=self.GetStudentId(pk))
        serializer.validated_data["is_approved"] = "W"
        serializer.validated_data["student"] = student
        serializer.save()

    def GetStudentId(self, pk):
        try:
            pk = int(pk)
            return str(pk)
        except:
            return Student.objects.get(user_ptr_id=self.request.user.id).id


class RetrieveRestorationRequestView(generics.RetrieveAPIView):
    serializer_class = RetrieveRestorationRequestSerializer

    def get_object(self):
        pk = self.kwargs['pk']
        student = Student.objects.get(pk=self.GetStudentId(pk))
        queryset = RestorationRequest.objects.filter(student=student).order_by('-submitted_date')
        return queryset.first()

    def GetStudentId(self, pk):
        try:
            pk = int(pk)
            return str(pk)
        except:
            return Student.objects.get(user_ptr_id=self.request.user.id).id
