from django.contrib import admin
from .models import ApprovedCourse, SemesterCourse, CourseAndStudent

# Register the models with the admin site
admin.site.register(ApprovedCourse)
admin.site.register(SemesterCourse)
admin.site.register(CourseAndStudent)
