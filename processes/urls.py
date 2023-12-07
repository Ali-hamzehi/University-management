from django.urls import path
from .views import *


urlpatterns = [
    path("student/<int:student_pk>/courses/<int:course_pk>/appeal-request/",
         StudentListCreateAppealRequest.as_view()),
    path("student/<int:student_pk>/courses/<int:course_pk>/appeal-request/<int:pk>/",
         StudentRetrieveUpdateDestroyAppealRequest.as_view()),
    path("professor/<int:professor_id>/courses/<int:course_pk>/appeal-requests/",
         ProfessorListAppealRequest.as_view()),
    path("professor/<int:professor_id>/courses/<int:course_pk>/appeal-requests/<int:pk>/",
         ProfosserRetrieveUpdateDestroyAppealRequest.as_view()),
    path("professor/<int:professor_id>/courses/<int:course_pk>/approve/",ApproveGradesAPIView.as_view(),name="ApproveGrades"),
    path("student/<int:student_pk>/studying-evidence/",
         ListCreateStudyingEvidence.as_view(), name="StudyingEvidence"),
    path('student/<int:student_pk>/studying-evidence/<int:pk>/',
         RetrieveUpdateDestroyStudyingEvidence.as_view(), name="StudyingEvidence-detail"),
    path('assistant/<int:student_pk>/studying-evidence/',
         AssistantListStudyingEvidence.as_view(), name="Assistant-StudyingEvidence"),
    path('assistant/<int:student_pk>/studying-evidence/<int:pk>/',
         AssistantRetriveUpdateStudingEvidence.as_view(), name="Assistant-StudyingEvidence-detail"),
    path('assistant/<int:assistant_id>/courses/<int:pk>/prof-approved/', ApprovedCoursesByProfessorsAPIView.as_view(), name='approved_courses_by_professors'),
    path('assistant/<int:assistant_id>/courses/<int:course_id>/professor/<int:professor_id>/approved/', CourseDetailByProfessorApprovalView.as_view(), name='course_detail_by_professor_approval'),
    # KIA:
    path('create-college/', CreateCollegeView.as_view(), name='create_college'),
    path('get-college-list/', GetCollegeListView.as_view(),
         name='get_college_list'),
    path('get-college-detail/<int:pk>/',
         GetCollegeDetailView.as_view(), name='get_college-detail'),
    path('update-college/<int:pk>/',
         UpdateCollegeView.as_view(), name='update_college'),
    path('delete-college/<int:pk>/',
         DeleteCollegeView.as_view(), name='delete_college'),
    # IDA:
    path("term/", TermListCreateView.as_view(), name="term-list-create"),
    path("term/<int:pk>/", TermDetailView.as_view(), name="term-list-detail"),
    # IDA & AH & KIA
    path("student/<int:pk>/course-selection/check/",
         UnitSelectionCheckView.as_view(), name='course-selection-check'),
    path("student/<int:pk>/course-selection/submit/",
         UnitSelectionSubmitView.as_view(), name='course-selection-submit'),
    path("student/<int:pk>/course-selection/send-form/",
         UnitSelectionSendFormView.as_view(), name='course-selection-send-form'),

    # AJ :
    path("student/<slug:pk>/course-selection/create/",
         CreateUnitSelectionRequestView.as_view(), name="Create-RestorationRequest-View"),
    # AK:
    path("professor/<int:professor_id>/students-selection-forms/",
         ProfessorStudentsSelectionFormsView.as_view(), name="List-UnitSelectionRequest-View"),
    path("professor/<int:professor_id>/students-selection-forms/<int:pk>/",
         ProfessorStudentsSelectionFormsDetailView.as_view(), name="Retrieve-UnitSelectionRequest-View"),
    path("professor/<int:professor_id>/students-substitution-forms/",
         ProfessorStudentsSubstitutionFormsView.as_view(), name="List-RestorationRequest-View"),
    path("professor/<int:professor_id>/students-substitution-forms/<int:pk>/",
         ProfessorStudentsSubstitutionFormsDetailView.as_view(), name="Retrieve-RestorationRequest-View"),
    path('professor/<int:professor_id>/students-substitution-forms/<int:pk>/',
         SubstitutionFormApprovalView.as_view(), name='substitution-form-approval'),
    path('professor/<int:professor_id>/students-selection-forms/<int:pk>/',
         SubstitutionFormApprovalView.as_view(), name='selection-form-approval'),


    # AJ
    path("student/<slug:pk>/course-substitution/create/",
         CreateUnitSelectionRequestView.as_view(), name="Create-UnitSelection-Request"),
    path("student/<slug:pk>/course-selection/",
         RetrieveUnitSelectionRequestView.as_view(), name='Retrieve-UnitSelection-Request'),
    path("student/<slug:pk>/course-substitution/",
         CreateRestorationRequestView.as_view(), name="Create-Restoration-Request"),
    path("student/<slug:pk>/course-substitution/",
         RetrieveRestorationRequestView.as_view(), name="Retrieve-Restoration-Request"),

    # IDA
    path("student/<int:pk>/remove-term/", StudentEmergencyRemovalSemesterRequest.as_view(), name="Student-Removal-Semester"),
    path("assistant/<int:pk>/remove-term/", AssistantEmergencyRemovalSemesterVistView.as_view(), name="Assistant-Removal-Semester"),
    path("assistant/<int:pk>/remove-term/<int:s_pk>/", AssistantEmergencyRemovalSemesterDetail.as_view(), name="Assistant-Removal-Semester-Detail"),
     # AH
     path("student/<int:pk>/courses/<int:c_pk>/emergency-remove/",StudentEmergencyCourseRemovalRequestView.as_view(),name="Student-Removal-Course"),
     path("assistant/<int:pk>/emergency-remove/", AssistantEmergencyRemoveCourseListView.as_view(),name="Assistant-Removal-Course"),
     path("assistant/<int:pk>/emergency-remove/<int:s_pk>/",  AssistantEmergencyRemoveCourseDetailView.as_view(),name="Assistant-Removal-Semester-Detail")
]
