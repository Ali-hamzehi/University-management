from .models import *
from rest_framework import serializers


class ApprovedCourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = ApprovedCourse
        fields = '__all__'


class SemesterCourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = SemesterCourse
        fields = '__all__'
