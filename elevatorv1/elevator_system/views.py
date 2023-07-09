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
    
    def get_all_request_of_elevator(self, request, elevator_id=None):
        elevator = self.get_object()
        all_requests = elevator.requests.all()
        floor_list = [req.floor for req in all_requests]
        return Response({'floor_list': floor_list})

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
    
    
    def calculate_time_to_reach_floor(self, elevator, floor):
        if elevator.direction == 'up':
            if floor >= elevator.current_floor:
                return abs(floor - elevator.current_floor)
            else:
                return 2 * (elevator.current_floor - floor)  # Time to reach the top floor and then come back down
        elif elevator.direction == 'down':
            if floor <= elevator.current_floor:
                return abs(floor - elevator.current_floor)
            else:
                return 2 * (elevator.current_floor - floor)  # Time to reach the bottom floor and then come back up
        else:
            return abs(floor - elevator.current_floor)


class RequestViewSet(viewsets.ModelViewSet):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer
    lookup_field = 'floor_id'

    def select_optimal_elevator(self, floor):
        elevators = Elevator.objects.all()
        optimal_elevator = None
        min_time = float('inf')

        for e in elevators:
            time = self.calculate_time_to_reach_floor(e, floor)
            if time < min_time:
                min_time = time
                optimal_elevator = e

        return optimal_elevator
    

    def add_request_for_floor(self, request, floor_id):
        optimal_elevator = self.select_optimal_elevator(floor_id)
        has_requests = optimal_elevator.requests.exists()
        new_request = Request.objects.create(floor=floor_id)
        if has_requests:
            all_requests = optimal_elevator.requests.all()
            existing_floor_list = [req.floor for req in all_requests]
            if floor_id not in existing_floor_list:
                floor_list  = self.update_list_of_request_in_elevator(optimal_elevator, floor_id, existing_floor_list)
            # Clear existing requests
            optimal_elevator.requests.clear()

            # Create new Request objects and associate them with the optimal elevator
            for new_floor in floor_list:
                new_request = Request.objects.create(floor=new_floor)
                optimal_elevator.requests.add(new_request)
                # optimal_elevator.requests.set(floor_list)    
        else:
            optimal_elevator.requests.add(new_request)
        optimal_elevator.save()
        return Response({'message': f'Request added for {optimal_elevator}'})


    def update_list_of_request_in_elevator(self, optimal_elevator, floor_requested, floor_list):
        optimal_current_floor = optimal_elevator.current_floor
        optimal_direction = optimal_elevator.direction
        if optimal_current_floor not in floor_list:
            floor_list.insert(0, optimal_current_floor)

        if floor_requested in floor_list:
            return floor_list

        if len(floor_list) == 0:
                floor_list.append(floor_requested)
        elif floor_requested >= floor_list[0]:
            index = 0
            while index < len(floor_list) and floor_requested >= floor_list[index]:
                index += 1
            floor_list.insert(index, floor_requested)
        else:
            index = 0
            while index < len(floor_list) and floor_requested <= floor_list[index]:
                index += 1
            floor_list.insert(index, floor_requested)

        return floor_list


    
    def calculate_time_to_reach_floor(self, elevator, floor):
        if elevator.direction == 'up':
            if floor >= elevator.current_floor:
                return abs(floor - elevator.current_floor)
            else:
                return 2 * (elevator.current_floor - floor)  # Time to reach the top floor and then come back down
        elif elevator.direction == 'down':
            if floor <= elevator.current_floor:
                return abs(floor - elevator.current_floor)
            else:
                return 2 * (elevator.current_floor - floor)  # Time to reach the bottom floor and then come back up
        else:
            return abs(floor - elevator.current_floor)

class AddElevatorView(viewsets.ModelViewSet):
    def new_elevator(self, request):
        serializer = ElevatorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    

class DeleteElevatorView(viewsets.ModelViewSet):
    def delete_elevator(self, request, elevator_id):
        try:
            elevator = Elevator.objects.get(elevator_id=elevator_id)
            elevator.delete()
            return Response({"message" : "deleted successfully"}, status=204)
        except Elevator.DoesNotExist:
            return Response({"error": "Elevator does not exist."}, status=404)
        

class ReinitializeElevatorSystemView(viewsets.ModelViewSet):
    def reinitialise(self, request):
        # Get all elevator objects
        elevators = Elevator.objects.all()

        # Reset the state of each elevator to the default values
        for elevator in elevators:
            elevator.status = "stopped"
            elevator.current_floor = 1
            elevator.direction = "stopped"
            elevator.requests.clear()
            elevator.save()

        return Response({"message": "Elevator system reinitialized successfully."})