from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Elevator, Request
from .serializers import ElevatorSerializer, RequestSerializer

class ElevatorViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.elevator = Elevator.objects.create(status="stopped", current_floor=1, direction="stopped")
        self.elevator_serializer = ElevatorSerializer(instance=self.elevator)
        self.elev_id = self.elevator.elevator_id

        print("elevator id ", self.elev_id)

    def test_initialize_system(self):
        url = '/elevators/initialize_system/'
        response = self.client.post(url, {'num_elevators': 1}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data), 1)

    def test_get_all_request_of_elevator(self):
        url = f'/elevators/{self.elev_id}/get_floor_list/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['floor_list'], [])

    def test_get_direction(self):
        url = f'/elevators/{self.elev_id}/direction/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['direction'], self.elevator.direction)

    # def test_mark_maintenance(self):
    #     url = f'/elevators/{self.elevator.elevator_id}/mark_maintenance/'
    #     response = self.client.put(url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.data['message'], f'{self.elevator} marked as maintenance')
    #     updated_elevator = Elevator.objects.get(elevator_id=self.elevator.elevator_id)
    #     self.assertEqual(updated_elevator.status, 'maintenance')

    # def test_open_door(self):
    #     url = f'/elevators/{self.elevator.elevator_id}/open_door/'
    #     response = self.client.put(url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.data['message'], f'{self.elevator} door opened')
    #     updated_elevator = Elevator.objects.get(elevator_id=self.elevator.elevator_id)
    #     self.assertTrue(updated_elevator.door_open)

    # def test_close_door(self):
    #     url = f'/elevators/{self.elevator.elevator_id}/close_door/'
    #     response = self.client.put(url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.data['message'], f'{self.elevator} door closed')
    #     updated_elevator = Elevator.objects.get(elevator_id=self.elevator.elevator_id)
    #     self.assertFalse(updated_elevator.door_open)

    def test_request_elevator_to_floor(self):
        url = f'/elevators/{self.elev_id}/request_floor/'
        response = self.client.post(url, {'floor_id': 5}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], f'floor added for {self.elevator}')
        updated_elevator = Elevator.objects.get(elevator_id=self.elev_id)
        self.assertEqual(updated_elevator.requests.count(), 2)
        self.assertEqual(updated_elevator.requests.first().floor, 1)

class RequestViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.elevator = Elevator.objects.create(status="stopped", current_floor=1, direction="stopped")
        self.request = Request.objects.create(floor=5, elevator=self.elevator)
        self.request_serializer = RequestSerializer(instance=self.request)
        self.elev_id = self.elevator.elevator_id

    def test_add_request_for_floor(self):
        url = f'/elevators/{self.elev_id}/request_floor/'
        response = self.client.post(url, {'floor_id': 5}, format='json')
        url = f'/elevators/{self.elev_id}/get_floor_list/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['floor_list'], [1, self.request.floor])


class AddElevatorViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_new_elevator(self):
        url = '/elevators/add/'
        data = {
            'status': 'stopped',
            'current_floor': 1,
            'direction': 'stopped'
        }

        response = self.client.post(url, data, format='json')
        print("response : ", self.client)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Elevator.objects.filter(elevator_id=response.data['elevator_id']).exists())

class DeleteElevatorViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.elevator = Elevator.objects.create(status="stopped", current_floor=1, direction="stopped")

    def test_delete_elevator(self):
        url = f'/elevators/{self.elevator.elevator_id}/delete/'
        response = self.client.delete(url)