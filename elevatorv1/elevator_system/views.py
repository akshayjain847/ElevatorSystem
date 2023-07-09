from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Elevator, Request
from .serializers import ElevatorSerializer, RequestSerializer

class ElevatorViewSet(viewsets.ModelViewSet):
    queryset = Elevator.objects.all()
    serializer_class = ElevatorSerializer
    lookup_field = 'elevator_id'

    @staticmethod
    def initialize_system(request):
        num_elevators = request.data.get('num_elevators', 1)
        elevators = []
        for _ in range(num_elevators):
            elevator = Elevator.objects.create()
            elevators.append(elevator)
        serializer = ElevatorSerializer(elevators, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_next_destination_floor(self, request, elevator_id=None):
        elevator = self.get_object()
        # Implement the logic to fetch the next destination floor for the given elevator
        next_floor = 0  # Replace with the actual logic
        return Response({'next_floor': next_floor})

    def get_direction(self, request, elevator_id=None):
        elevator = self.get_object()
        return Response({'direction': elevator.direction})

    def add_request(self, request, elevator_id=None):
        elevator = self.get_object()
        floor = request.data.get('floor')
        new_request = Request.objects.create(floor=floor)
        elevator.requests.add(new_request)
        elevator.save()
        return Response({'message': f'Request added for {elevator}'})

    def mark_maintenance(self, request, elevator_id=None):
        elevator = self.get_object()
        elevator.status = 'maintenance'
        elevator.save()
        return Response({'message': f'{elevator} marked as maintenance'})

    def open_door(self, request, elevator_id=None):
        elevator = self.get_object()
        elevator.open_door()
        elevator.save()
        return Response({'message': f'{elevator} door opened'})

    def close_door(self, request, elevator_id=None):
        elevator = self.get_object()
        elevator.close_door()
        elevator.save()
        return Response({'message': f'{elevator} door closed'})


class RequestViewSet(viewsets.ModelViewSet):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer
