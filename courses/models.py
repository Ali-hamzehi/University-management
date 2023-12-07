from django.db import models
from django_jalali.db import models as jmodels


class ApprovedCourse(models.Model):
    approved_course_id = models.IntegerField(auto_created=True, primary_key=True)
    course_name = models.CharField(max_length=50)
    provider_college = models.ForeignKey('processes.College', related_name="provider_college_forgain", on_delete=models.CASCADE)
    prerequisites = models.ManyToManyField('ApprovedCourse', related_name="courses_that_need_this_course", blank=True)
    both_needs = models.ManyToManyField('ApprovedCourse', related_name="courses_required_for_this_course", blank=True)
    number_of_course_units = models.IntegerField()
    course_type = models.CharField(max_length=50)

    def __str__(self):
        return self.course_name


class SemesterCourse(models.Model):
    approved_course = models.ForeignKey('ApprovedCourse', on_delete=models.CASCADE, related_name='approved_course')
    semester_course_id = models.IntegerField(auto_created=True, primary_key=True)
    class_day_and_time = models.CharField(max_length=50)
    exam_date_and_time = jmodels.jDateTimeField()
    exam_location = models.CharField(max_length=50)
    course_professor = models.ForeignKey('users.Professor', on_delete=models.SET_NULL, null=True,
                                         related_name="professor_course", blank=True)
    course_capacity = models.IntegerField(blank=True, null=True)
    current_semester = models.ForeignKey('processes.Semester', on_delete=models.SET_NULL, null=True,
                                         related_name="semester_course", blank=True)

    def __str__(self):
        return str(self.semester_course_id)


class CourseAndStudent(models.Model):
    course_status = models.CharField(max_length=50)
    student_score = models.FloatField()
    semester_taken = models.IntegerField()


class StudentGrade(models.Model):
    course = models.ForeignKey(SemesterCourse, on_delete=models.CASCADE)
    student = models.ForeignKey('users.Student', on_delete=models.CASCADE)
    grade = models.FloatField()
    course_status = models.CharField(max_length=50)
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"course : {self.course} grade {self.grade}"
