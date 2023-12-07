from django.urls import path
from .views import *

urlpatterns = [
    path("subjects/", ApprovedCourseListCreateView.as_view(), name="approved-course-list"),
    path("subjects/<int:pk>/", ApprovedCoursesDetailView.as_view(), name="approved-courses-detail"),
    path("courses/", SemesterCourseListCreateView.as_view(), name="semester-course-list"),
    path("courses/<int:pk>/", SemesterCourseDetailView.as_view(), name="semester-course-detail"),
]
