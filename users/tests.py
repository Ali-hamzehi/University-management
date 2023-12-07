from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import *
from processes.models import *
from jdatetime import datetime


class StudentListCreateViewTest(APITestCase):

    def setUp(self):
        self.semester = Semester.objects.create(
            semester_id=1,
            semester_name=1,
            unit_selection_start_time=datetime(1400, 1, 1),
            unit_selection_end_time=datetime(1400, 1, 1),
            classes_start_time=datetime(1400, 1, 1),
            classes_end_time=datetime(1400, 1, 1),
            restoration_start_time=datetime(1400, 1, 1),
            restoration_end_time=datetime(1400, 1, 1),
            emergency_removal_end_time=datetime(1400, 1, 1),
            exams_start_time=datetime(1400, 1, 1),
            semester_end_time=datetime(1400, 1, 1),
            semester_courses_list="Your semester courses list here")
        self.url = reverse('student-list')

    def test_create_and_get_student(self):
        data = {
            "user_number": 105,
            "username": "test_user_api",
            "first_name": "Test1",
            "last_name": "User1",
            "password": "testpassword",
            "phone_number": "1234567890",
            "national_id": "ABC1234567",
            "gender": "M",
            "birth_date": "2000-01-01",
            "kind": "S",
            "entry_semester": "401",
            "current_semester": 1,
            "gpa": 17.9,
            "supervisor": "Professor1",
            "military_service_status": False,
            "sanavat": 2
        }

        create_response = self.client.post(self.url, data, format='json')
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)

        new_student_id = create_response.data.get('user_number')
        get_url = reverse('student-detail', kwargs={'pk': new_student_id})
        get_response = self.client.get(get_url)
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)


class StudentDetailViewTest(APITestCase):
    def setUp(self):
        self.semester = Semester.objects.create(
            semester_id=2,
            semester_name=406,
            unit_selection_start_time=datetime(1400, 1, 1),
            unit_selection_end_time=datetime(1400, 1, 1),
            classes_start_time=datetime(1400, 1, 1),
            classes_end_time=datetime(1400, 1, 1),
            restoration_start_time=datetime(1400, 1, 1),
            restoration_end_time=datetime(1400, 1, 1),
            emergency_removal_end_time=datetime(1400, 1, 1),
            exams_start_time=datetime(1400, 1, 1),
            semester_end_time=datetime(1400, 1, 1),
            semester_courses_list="Your semester courses list here")

        self.student_data = {
            "user_number": 106,
            "username": "test_user",
            "first_name": "Test1",
            "last_name": "User1",
            "password": "testpassword",
            "phone_number": "1234567890",
            "national_id": "ABC1234567",
            "gender": "M",
            "birth_date": "2000-01-01",
            "kind": "S",
            "entry_semester": "401",
            "current_semester": self.semester,
            "gpa": 17.9,
            "supervisor": "Professor1",
            "military_service_status": False,
            "sanavat": 2
        }
        self.student = Student.objects.create(**self.student_data)
        self.student.current_semester = self.semester
        self.student.save()

    def test_retrieve_student_detail(self):
        url = reverse('Get-Student', kwargs={'pk': self.student.user_number})
        response = self.client.get(url)

        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user_number'], self.student.user_number)
        self.assertEqual(response.data['phone_number'], self.student.phone_number)
        self.assertEqual(response.data['first_name'], self.student.first_name)

    def test_update_student_detail(self):
        url = reverse('Get-Student', kwargs={'pk': self.student.user_number})
        update_data = {
            "user_number": 106,
            "username": "test_user",
            "first_name": "Test1",
            "last_name": "User1",
            "password": "newpassword",
            "phone_number": "1234567894",
            "national_id": "ABC1234567",
            "gender": "M",
            "birth_date": "2000-01-01",
            "kind": "S",
            "entry_semester": "401",
            "current_semester": self.semester.semester_id,
            "gpa": 17.9,
            "supervisor": "Professor1",
            "military_service_status": False,
            "sanavat": 2
        }
        response = self.client.put(url, update_data, format='json', partial=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_student = Student.objects.get(user_number=self.student.user_number)
        self.assertEqual(updated_student.phone_number, update_data['phone_number'])
        self.assertNotEqual(updated_student.password, update_data['password'])

    def test_delete_student(self):
        url = reverse('Get-Student', kwargs={'pk': self.student.user_number})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(Student.DoesNotExist):
            Student.objects.get(user_number=self.student.user_number)

