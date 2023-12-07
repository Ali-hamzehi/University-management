from courses.models import SemesterCourse, StudentGrade
from rest_framework import serializers
from users.models import Professor
from users.models import Professor
from .models import *
from users.models import Student, User


class CollegeSerializer(serializers.ModelSerializer):
    class Meta:
        model = College
        fields = "__all__"


class StudentAppealRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppealRequest
        exclude = ['submitted_date']
        extra_kwargs = {
            "appeal_answer": {"read_only": True}
        }
class ApproveGradesSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentGrade
        fields = '__all__'

class SemesterCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = SemesterCourse
        fields = '__all__'

class SemesterCourseDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = SemesterCourse
        fields = '__all__'
class ProfessorAppealRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppealRequest
        fields = '__all__'
        extra_kwargs = {
            "student": {"read_only": True},
            "course": {"read_only": True},
            "appeal_text": {"read_only": True},
            "submitted_date": {"read_only": True}
        }


class StudyingEvidenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmploymentInSpecialEducationForBoysRequest
        fields = "__all__"


class TermSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semester
        fields = '__all__'


class RemovalSemesterRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmergencyRemovalSemesterRequest
        fields = '__all__'

    # def update(self, instance, validated_data):
    #     if self.context['request'].user.is_educational_assistant:
    #         instance.is_approved = validated_data.get('request_result', instance.is_approved)
    #         instance.save()
    #     return instance
class EmergencyCourseRemovalRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = EmergencyRemovalSemesterRequest
        fields = '__all__'

class UnitSelectionRequestSerializer(serializers.ModelSerializer):
    requested_courses = serializers.ListField(
        child=serializers.IntegerField(), 
        write_only=True,
    )
    class Meta:
        model = UnitSelectionRequest
        fields = "__all__"
    def create(self, validated_data):
        requested_courses_ids = validated_data.pop('requested_courses', [])
        instance = super().create(validated_data)

        requested_courses = SemesterCourse.objects.filter(
            semester_course_id__in=requested_courses_ids
        )

        instance.requested_courses.set(requested_courses)
        return instance
    def validate_unitnumber(self, data):
        course_unit_counter = 0
        for course in data.requested_courses:
            course_unit_counter += course.approved_course.number_of_course_units

        gpa = data.student.gpa
        if gpa <= 17:
            if course_unit_counter > 20:
                raise serializers.ValidationError(
                    'The number of units requested is more than the allowed limit.')
        elif course_unit_counter > 24:
            raise serializers.ValidationError(
                'The number of units requested is more than the allowed limit.')

        if course_unit_counter < 12:
            raise serializers.ValidationError(
                'The number of units requested is less than the allowed limit.')

        return data

    def validate_prerequisites(self, data):
        for course in data.requested_courses:
            for prerequisites in course.approved_course.prerequisites:
                if prerequisites not in data.student.passed_courses:
                    raise serializers.ValidationError(
                        'The prerequisite course must have been completed.')

        return data

    def validate_RepeatedOrPassed(self, data):
        for course in data.requested_courses:
            if course.approved_course in data.student.passed_courses:
                raise serializers.ValidationError(
                    'Repeated or passed lessons should not be taken.')

        for course1 in data.requested_courses:
            counter = 0
            for course2 in data.requested_courses:
                if course1 == course2:
                    counter += 1
            if counter > 1:
                raise serializers.ValidationError(
                    'Repeated or passed lessons should not be taken.')

        return data

    def validate_CourseCapacity(self, data):

        for course in data.requested_courses:
            if course.course_capacity == 0:
                raise serializers.ValidationError(
                    'The capacity of the course is completed.')

        return data

    def validate_ExamAnClassTime(self, data):

        for course1 in data.requested_courses:
            for course2 in data.requested_courses:
                if course1 != course2:
                    if course1.exam_date_and_time == course2.exam_date_and_time:
                        raise serializers.ValidationError(
                            'Exam times interfere.')

        for course1 in data.requested_courses:
            for course2 in data.requested_courses:
                if course1 != course2 and course1.class_day == course2.class_day:
                    if course2.class_start_time <= course1.class_start_time <= course2.class_end_time:
                        raise serializers.ValidationError(
                            'Class times interfere.')
                    elif course2.class_start_time <= course1.class_end_time <= course2.class_end_time:
                        raise serializers.ValidationError(
                            'Class times interfere.')

        return data

    def validate_sanavat(self, data):
        if data.student.sanavat == 0:
            raise serializers.ValidationError('You have no sanavat.')

        return data


class CreateUnitSelectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnitSelectionRequest
        fields = ("requested_courses", "is_approved", "student")
        read_only_fields = ("is_approved", "student")


class UnitSelectionFormSerializer(serializers.ModelSerializer):
    first_name = serializers.StringRelatedField()
    last_name = serializers.StringRelatedField()

    class Meta:
        model = Student
        fields = ['id', 'first_name', 'last_name']


class UnitSelectionRequestFormDetailSerializer(serializers.ModelSerializer):
    first_name = serializers.StringRelatedField(source='student.first_name')
    last_name = serializers.StringRelatedField(source='student.last_name')

    class Meta:
        model = UnitSelectionRequest
        fields = "__all__"


class RestorationRequestFormSerializer(serializers.ModelSerializer):
    first_name = serializers.StringRelatedField()
    last_name = serializers.StringRelatedField()

    class Meta:
        model = Student
        fields = ['id', 'first_name', 'last_name']


class RestorationRequestFormDetailSerializer(serializers.ModelSerializer):
    first_name = serializers.StringRelatedField(source='student.first_name')
    last_name = serializers.StringRelatedField(source='student.last_name')

    class Meta:
        model = RestorationRequest
        fields = "__all__"


class ProfessorSelectionForm(serializers.ModelSerializer):
    first_name = serializers.StringRelatedField(source='student.first_name')
    last_name = serializers.StringRelatedField(source='student.last_name')

    class Meta:
        model = UnitSelectionRequest
        fields = "__all__"


class ProfessorSubstitutionFormSerializer(serializers.ModelSerializer):
    first_name = serializers.StringRelatedField(source='student.first_name')
    last_name = serializers.StringRelatedField(source='student.last_name')

    class Meta:
        model = RestorationRequest
        fields = "__all__"


class CreateUnitSelectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnitSelectionRequest
        fields = ("requested_courses", "is_approved", "student")
        read_only_fields = ("is_approved", "student")

class RetrieveUnitSelectionRequestSerializer(serializers.ModelSerializer):
    class Meta :
        model = UnitSelectionRequest
        fields = '__all__'
        

class CreateRestorationRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestorationRequest
        fields = ("requested_courses", "is_approved", "student","added_courses","dropped_courses")
        read_only_fields = ("is_approved", "student")


class RetrieveRestorationRequestSerializer(serializers.ModelSerializer):
    class Meta :
        model = RestorationRequest
        fields = '__all__'