from .models import User, Student, Professor, EducationalAssistant, ITmanager
from rest_framework import serializers
from processes.models import College, Semester
from courses.models import ApprovedCourse, SemesterCourse
from django.contrib.auth.hashers import make_password


class AssistantSerializer(serializers.ModelSerializer):
    college = serializers.StringRelatedField(many=True, read_only=True)
    field = serializers.StringRelatedField(many=True, read_only=True)
    avatar = serializers.ImageField(required=False)
    password = serializers.CharField(write_only=True, required=True, style={
        'input_type': 'password'})

    class Meta:
        model = EducationalAssistant
        exclude = ('last_login', 'groups', 'user_permissions', 'date_joined', 'is_staff', 'is_active')


class StudentSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(required=False)
    password = serializers.CharField(write_only=True, required=True, style={
        'input_type': 'password'})

    class Meta:
        model = Student
        exclude = ('last_login', 'groups', 'user_permissions', 'date_joined', 'is_staff', 'is_active')


class ProfessorSerializer(serializers.ModelSerializer):
    user_id = serializers.CharField(read_only=True)

    class Meta:
        model = Professor
        exclude = ('last_login', 'groups', 'user_permissions', 'date_joined', 'is_staff', 'is_active')


class SemesterListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semester
        fields = ("semester_name", "id")


class SemesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semester
        fields = "__all__"


class PickableCoursesSerializers(serializers.ModelSerializer):
    class Meta:
        model = ApprovedCourse
        fields = ("course_name", "provider_college")


class SanavatSerializers(serializers.Serializer):
    sanavat = serializers.IntegerField()


class CreateProfessorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professor
        fields = "__all__"

    def validate_password(self, value):
        if value:
            value = make_password(value)
        return value


class ChangePasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField()
    repeat_password = serializers.CharField()

    def validate(self, attrs):
        new_password = attrs.get('new_password')
        repeat_password = attrs.get('repeat_password')
        if new_password != repeat_password:
            raise serializers.ValidationError("The new password and repeat password must match.")

        return attrs
        
         
class CourseScheduleSerializer(serializers.ModelSerializer):

    class Meta:
        model = SemesterCourse
        fields = ('approved_course.course_name', 'class_day_and_time')

class CourseExamSerializer(serializers.ModelSerializer):

    class Meta:
        model = SemesterCourse
        fields = ('exam_date_and_time', 'exam_location')

    
    
