from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from users.models import ITmanager, EducationalAssistant
from processes.models import *
from courses.models import ApprovedCourse
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import get_user_model


# C Endpoints - Subjects & Courses
class ApprovedCourseListCreateViewTest(APITestCase):
    def setUp(self):
        self.college = College.objects.create(
            college_id=301,
            college_name="azad"
        )
        self.field = Field.objects.create(
            field_id=401,
            field_name="computer",
            educational_group="computer",
            college=self.college,
            number_of_units=140,
            degree="master"
        )
        self.ITmanager = get_user_model().objects.create_user(
            user_number=120,
            username="it_man",
            first_name="Test1",
            last_name="User1",
            password=make_password('it_manager_password'),
            phone_number="1234567890",
            national_id="ABC1234567",
            gender="M",
            birth_date="2000-01-01",
            kind="I"
        )

        self.educational_assistant = EducationalAssistant.objects.create(
            user_number=130,
            username="edu_assistant",
            first_name="Test2",
            last_name="User2",
            password=make_password('edu_assistant_password'),
            phone_number="1234567890",
            national_id="ABC1234567",
            gender="M",
            birth_date="2000-01-01",
            kind="E",
            college=self.college,
            field=self.field,
        )

        self.course_data = {
            'approved_course_id': 501,
            'course_name': 'algorithm',
            'provider_college': self.college.college_id,
            'number_of_course_units': 3,
            'course_type': 'takhasosi'
        }

    def get_access_token(self, user):
        access_token = AccessToken.for_user(user)
        return {'Authorization': f'Bearer {access_token}'}

    def test_create_course_authenticated(self):
        url = reverse('approved-course-list')
        self.client.force_authenticate(user=self.ITmanager)
        self.client.force_authenticate(user=self.educational_assistant)
        response = self.client.post(url, self.course_data, format='json', partial=True)
        if response.status_code != status.HTTP_200_OK:
            print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_courses_authenticated(self):
        url = reverse('approved-course-list')
        self.client.force_authenticate(user=self.ITmanager)
        self.client.force_authenticate(user=self.educational_assistant)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ApprovedCoursesDetailViewTest(APITestCase):
    def setUp(self):
        self.college = College.objects.create(
            college_id=301,
            college_name="azad"
        )
        self.field = Field.objects.create(
            field_id=401,
            field_name="computer",
            educational_group="computer",
            college=self.college,
            number_of_units=140,
            degree="master"
        )
        self.ITmanager = get_user_model().objects.create_user(
            user_number=120,
            username="it_man",
            first_name="Test1",
            last_name="User1",
            password=make_password('it_manager_password'),
            phone_number="1234567890",
            national_id="ABC1234567",
            gender="M",
            birth_date="2000-01-01",
            kind="I"
        )

        self.educational_assistant = EducationalAssistant.objects.create(
            user_number=130,
            username="edu_assistant",
            first_name="Test2",
            last_name="User2",
            password=make_password('edu_assistant_password'),
            phone_number="1234567890",
            national_id="ABC1234567",
            gender="M",
            birth_date="2000-01-01",
            kind="E",
            college=self.college,
            field=self.field,
        )

        self.approved_course = ApprovedCourse.objects.create(
            approved_course_id=501,
            course_name='algorithm',
            provider_college=self.college,
            number_of_course_units=3,
            course_type='takhasosi'
        )

    def get_access_token(self, user):
        access_token = AccessToken.for_user(user)
        return {'Authorization': f'Bearer {access_token}'}

    def test_get_course_detail_authenticated(self):
        url = reverse('approved-courses-detail', kwargs={'pk': self.approved_course.approved_course_id})
        self.client.force_authenticate(user=self.ITmanager)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_course_authenticated(self):
        url = reverse('approved-courses-detail', kwargs={'pk': self.approved_course.approved_course_id})
        self.client.force_authenticate(user=self.educational_assistant)
        data = {
            'course_name': 'updated_algorithm',
            'provider_college': self.college.college_id,
            'number_of_course_units': 4,
            'course_type': 'updated_takhasosi'
        }
        response = self.client.put(url, data, format='json', partial=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['course_name'], 'updated_algorithm')
        self.assertEqual(response.data['number_of_course_units'], 4)

    def test_delete_course_authenticated(self):
        url = reverse('approved-courses-detail', kwargs={'pk': self.approved_course.approved_course_id})
        self.client.force_authenticate(user=self.ITmanager)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'message': 'course deleted'})
