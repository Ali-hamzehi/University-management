from django.contrib import admin
from .models import Semester, College, Field, UnitSelectionRequest, RestorationRequest, AppealRequest, \
    EmergencyRemovalCourseRequest, EmergencyRemovalSemesterRequest, EmploymentInSpecialEducationForBoysRequest

# Register your models with the admin site
admin.site.register(Semester)
admin.site.register(College)
admin.site.register(Field)
admin.site.register(UnitSelectionRequest)
admin.site.register(RestorationRequest)
admin.site.register(AppealRequest)
admin.site.register(EmergencyRemovalCourseRequest)
admin.site.register(EmergencyRemovalSemesterRequest)
admin.site.register(EmploymentInSpecialEducationForBoysRequest)
