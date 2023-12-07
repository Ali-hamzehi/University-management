from django.urls import path
from .views import *
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView,
                        TokenBlacklistView , TokenVerifyView)

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', TokenBlacklistView.as_view(),
         name='token_blacklist'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('change-password-request/',ChangePasswordRequest.as_view(),name="change-password-request"),
    path('change-password-action/<str:Token>',ChangePasswordAction.as_view(),name="change-password-action"),
    path("assistants/", AssistantListCreateView.as_view(),
         name="assistant-list"),
    path("assistants/<int:pk>/",
         AssistantDetailView.as_view(), name="assistant-detail"),
    path("admin/students/<int:pk>/", StudentDetailView.as_view(),
         name="student-detail"),
    path("admin/students/", StudentListCreateView.as_view(),
         name="student-list"),

    path("students/", StudentListVeiw.as_view(),name= "Student-List"),
    path("students/<int:pk>/",RetrieveUpdateStudentView.as_view(),name="Get-Student"),
    path("professors/",ProfessorListVeiw.as_view(),name="Professor-List"),
    path("Professor/<int:pk>/",RetrieveUpdateProfessorView.as_view(),name="Retrieve-Update-Professor"),
    path("terms/",SemesterListView.as_view(),name="Semester-List"),
    path("term/<int:pk>/",RetrieveSemester.as_view(),name="Retrieve-Semester"),

    path("student/<slug:pk>/my-courses/",PickableCourses.as_view(),name="Pickable-Courses"),
    path("student/<slug:pk>/pass-courses-report/",PassedCourseStatus.as_view(),name="Course-Status"),
    path("student/<slug:pk>/term-courses/",TermCourseStatus.as_view(),name="Term-Course-Status"),
    path("student/<slug:pk>/remaining-terms/",RemainingSanavat.as_view(),name="Remaining-Sanavat"),
    path("professors/",CreateGetProfessor.as_view(),name="create-list-professors"),
    path("professor/<int:pk>/",RetrieveUpdateDestroyprofessor.as_view(),name="Retrieve-Update-Destroy-professor"),

    path("student/<int:pk>/class-schedule/",SudentSemesterCourseShedule.as_view()),
    path("student/<int:pk>/exam-schedule/",SudentSemesterCourseExams.as_view()),
]
