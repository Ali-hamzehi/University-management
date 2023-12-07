# Generated by Django 4.1.4 on 2023-11-15 19:08

from django.db import migrations, models
import django.db.models.deletion
import django_jalali.db.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('processes', '__first__'),
        ('users', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApprovedCourse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_name', models.CharField(max_length=50)),
                ('number_of_course_units', models.IntegerField()),
                ('course_type', models.CharField(max_length=50)),
                ('both_needs', models.ManyToManyField(blank=True, related_name='courses_required_for_this_course', to='courses.approvedcourse')),
                ('prerequisites', models.ManyToManyField(blank=True, related_name='courses_that_need_this_course', to='courses.approvedcourse')),
                ('provider_college', models.ManyToManyField(related_name='provider_college', to='processes.college')),
            ],
        ),
        migrations.CreateModel(
            name='SemesterCourse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_day_and_time', models.CharField(max_length=50)),
                ('exam_date_and_time', django_jalali.db.models.jDateTimeField()),
                ('exam_location', models.CharField(max_length=50)),
                ('course_capacity', models.IntegerField()),
                ('approved_course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='approved_course', to='courses.approvedcourse')),
                ('course_professor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='professor_course', to='users.professor')),
                ('current_semester', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='semester_course', to='processes.semester')),
            ],
        ),
        migrations.CreateModel(
            name='CourseAndStudent',
            fields=[
                ('semestercourse_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='courses.semestercourse')),
                ('course_status', models.CharField(max_length=50)),
                ('student_score', models.FloatField()),
                ('semester_taken', models.IntegerField()),
            ],
            bases=('courses.semestercourse',),
        ),
        migrations.CreateModel(
            name='StudentGrade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade', models.FloatField()),
                ('is_confirmed', models.BooleanField(default=False)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.semestercourse')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.student')),
            ],
        ),
    ]
