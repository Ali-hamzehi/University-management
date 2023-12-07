from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import *


# B Endpoints - Term
class TermListCreateViewTest(APITestCase):

    def test_create_semester(self):
        data = {
            "semester_id": 3,
            "semester_name": 402,
            "semester_courses_list": "Course A, Course B, Course C",
            "unit_selection_start_time": "2023-12-01T08:00:00Z",
            "unit_selection_end_time": "2023-12-15T17:00:00Z",
            "classes_start_time": "2024-01-10T08:30:00Z",
            "classes_end_time": "2024-04-25T16:30:00Z",
            "restoration_start_time": "2024-04-26T08:00:00Z",
            "restoration_end_time": "2024-05-10T17:00:00Z",
            "emergency_removal_end_time": "2024-05-15T17:00:00Z",
            "exams_start_time": "2024-05-20T08:00:00Z",
            "semester_end_time": "2024-06-15T17:00:00Z"
        }

        url = reverse('term-list-create')
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        created_semester_id = response.data['semester_id']

        url = reverse('term-list-create') + f'?semester_id={created_semester_id}'
        get_response = self.client.get(url)

        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(get_response.data), 1)
        self.assertEqual(get_response.data[0]['semester_id'], created_semester_id)
