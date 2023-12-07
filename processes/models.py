from django.db import models
from django_jalali.db import models as jmodels
from courses.models import ApprovedCourse

APPROVED_CHOICES = (("W", "Wating"), ("A", "Accepet"), ("R", "Reject"))


class Semester(models.Model):
    semester_id = models.IntegerField(primary_key=True)
    semester_name = models.IntegerField()
    registered_students = models.ManyToManyField(
        "users.Student", related_name="semester", blank=True)
    registered_professors = models.ManyToManyField(
        "users.Professor", related_name="semester", blank=True)
    semester_courses_list = models.TextField()
    unit_selection_start_time = jmodels.jDateTimeField()
    unit_selection_end_time = jmodels.jDateTimeField()
    classes_start_time = jmodels.jDateTimeField()
    classes_end_time = jmodels.jDateTimeField()
    restoration_start_time = jmodels.jDateTimeField()
    restoration_end_time = jmodels.jDateTimeField()
    emergency_removal_end_time = jmodels.jDateTimeField()
    exams_start_time = jmodels.jDateTimeField()
    semester_end_time = jmodels.jDateTimeField()

    def __str__(self):
        return str(self.semester_name)


class College(models.Model):
    college_id = models.IntegerField(auto_created=True, primary_key=True)
    college_name = models.CharField(verbose_name=(
        "college name :"), max_length=50, blank=False, null=False)

    def __str__(self):
        return self.college_name


class Field(models.Model):
    field_id = models.IntegerField(auto_created=True, primary_key=True)
    field_name = models.CharField(
        max_length=50, blank=False, null=False, verbose_name=("field name :"))
    educational_group = models.CharField(
        max_length=50, blank=False, null=False, verbose_name=("educational group :"))
    college = models.ForeignKey('College', related_name="Field_collage", on_delete=models.CASCADE)
    number_of_units = models.PositiveIntegerField(blank=False, null=False)
    degree = models.CharField(max_length=50, verbose_name=("degree :"))
    units = models.ManyToManyField(ApprovedCourse, related_name="Field",blank=True)

    def __str__(self):
        return str(self.field_name)


class UnitSelection(models.Model):
    student = models.ForeignKey('users.Student', on_delete=models.CASCADE)
    semester = models.ForeignKey('Semester', on_delete=models.CASCADE,
                                 related_name='unit_selection')
    selection_course = models.ManyToManyField(
        'courses.SemesterCourse', related_name='unit_selection_course')


class UnitSelectionRequest(models.Model):
    student = models.ForeignKey('users.Student', on_delete=models.CASCADE)
    Semester = models.ForeignKey('Semester', on_delete=models.CASCADE)
    requested_courses = models.ManyToManyField(
        'courses.SemesterCourse', related_name="UnitSelectionRequest")
    submitted_date = models.DateTimeField(auto_now_add=True)
    is_approved = models.CharField(max_length=1, choices=APPROVED_CHOICES,default="w")

    def __str__(self):
        return f"Request by {self.student} submitted on {self.submitted_date}"


class RestorationRequest(models.Model):
    student = models.ForeignKey('users.Student', on_delete=models.CASCADE)
    added_courses = models.ManyToManyField(
        'courses.SemesterCourse', related_name='added_to_requests', blank=True)
    dropped_courses = models.ManyToManyField(
        'courses.SemesterCourse', related_name='dropped_from_requests', blank=True)
    submitted_date = models.DateTimeField(auto_now_add=True)
    is_approved = models.CharField(max_length=1, choices=APPROVED_CHOICES)

    def __str__(self):
        return f"Repair Request by {self.student} submitted on {self.submitted_date}"


class AppealRequest(models.Model):
    student = models.ForeignKey('users.Student', on_delete=models.CASCADE)
    course = models.ForeignKey(
        'courses.SemesterCourse', on_delete=models.CASCADE)
    appeal_text = models.TextField()
    appeal_answer = models.TextField(blank=True)
    submitted_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reconsideration Request by {self.student} for {self.course} submitted on {self.submitted_date}"


class EmergencyRemovalCourseRequest(models.Model):
    applicant_student = models.ForeignKey('users.Student', on_delete=models.CASCADE,
                                          related_name='emergency_removal_course_requests_as_applicant')
    educational_assistant = models.ForeignKey('users.EducationalAssistant', on_delete=models.CASCADE,
                                              related_name='emergency_removal_semester_requests_aseducational_assistant')
    course = models.ForeignKey('courses.SemesterCourse', on_delete=models.CASCADE,
                               related_name='emergency_removal_course_requests_for_course')
    student_description = models.TextField()
    request_result = models.CharField(max_length=1, choices=APPROVED_CHOICES)



class EmergencyRemovalSemesterRequest(models.Model):
    applicant_student = models.ForeignKey('users.Student', on_delete=models.CASCADE,
                                          related_name='emergency_removal_semester_requests_as_applicant')
    educational_assistant = models.ForeignKey('users.EducationalAssistant', on_delete=models.CASCADE,
                                              related_name='emergency_removal_semester_requests_aseducational_assistant')
    semester = models.ForeignKey('processes.Semester', on_delete=models.CASCADE,
                                 related_name='emergency_removal_semester_requests_for_semester')
    student_description = models.TextField()
    request_result = models.CharField(max_length=1, choices=APPROVED_CHOICES)


class EmploymentInSpecialEducationForBoysRequest(models.Model):
    applicant_student = models.ForeignKey('users.Student', on_delete=models.CASCADE,
                                          related_name='employment_requests_as_applicant')
    study_employment_file = models.FileField(null=True, blank=True)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE,
                                 related_name='employment_requests_for_semester')
    student_description = models.TextField()
    certificate_issuance_location = models.CharField(max_length=100)
