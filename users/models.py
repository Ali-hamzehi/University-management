from datetime import date
from django.db import models
from django_jalali.db import models as jmodels
from django.contrib.auth.models import AbstractUser

PROFESSORS_RANK_CHOICES = (("Assistant", "Assistant Professor"),
                           ("Associate", "Associate Professor"),
                           ("Full", "Full Professor"))

GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
)

KIND_CHOICE = (
    ('S', 'Student'),
    ('P', 'Professor'),
    ('I', 'ITmanager'),
    ('E', 'Educational Assistant'),
)


class User(AbstractUser):
    user_number = models.PositiveSmallIntegerField(default=1, primary_key=True)
    avatar = models.ImageField(null=True, blank=True)
    phone_number = models.CharField(max_length=11)
    national_id = models.CharField(max_length=10)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    birth_date = jmodels.jDateField(default=date.today)
    kind = models.CharField(max_length=1, choices=KIND_CHOICE)

    def __str__(self):
        return self.username


class Student(User):
    entry_year = jmodels.jDateField(null=True, blank=True)
    entry_semester = models.CharField(max_length=3)
    current_semester = models.ForeignKey("processes.Semester", on_delete=models.CASCADE)
    gpa = models.FloatField()
    college = models.ForeignKey(
        'processes.College', on_delete=models.CASCADE, related_name='student_college', null=True)
    study_field = models.ManyToManyField(
        'processes.Field', related_name="Students", blank=True)
    passed_courses = models.ForeignKey(
        'courses.SemesterCourse', related_name='passed_course', on_delete=models.CASCADE, blank=True, null=True)
    in_progress_courses = models.ForeignKey(
        'courses.SemesterCourse', related_name='in_progress_courses', on_delete=models.CASCADE, blank=True, null=True)
    supervisor = models.CharField(max_length=30)
    military_service_status = models.BooleanField()
    sanavat = models.PositiveSmallIntegerField()


    class Meta:
        db_table = "Student"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Professor(User):
    college = models.ManyToManyField(
        'processes.College', related_name="Professors")
    field = models.ManyToManyField(
        'processes.Field', related_name="Professors")
    expertise = models.CharField(max_length=50)
    rank = models.CharField(max_length=10, choices=PROFESSORS_RANK_CHOICES)
    past_teaching_courses = models.TextField()
    current_semester = models.ForeignKey(
        'processes.Semester', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = "Professor"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class ITmanager(User):
    class Meta:
        db_table = "ITmanager"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class EducationalAssistant(User):
    college = models.ForeignKey('processes.College', related_name="edu_collage", on_delete=models.CASCADE)
    field = models.ForeignKey('processes.Field', related_name="edu_field", on_delete=models.CASCADE)

    class Meta:
        db_table = "EducationalAssistant"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
