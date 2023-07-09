import threading
import time
from django.core.management.base import BaseCommand
from elevator_system.models import Elevator

class ElevatorThread(threading.Thread):
    def __init__(self, elevator):
        super().__init__()
        self.elevator = elevator

    def run(self):
        while True:
            current_floor = self.elevator.current_floor
            direction = self.elevator.direction
            requests = self.elevator.requests.all()


            print(f"Elevator {self.elevator.elevator_id} - Current Floor: {current_floor}, Direction: {direction}")
            print(f"Requests: {requests}")

            if requests:
                next_floor = requests.first().floor
                if next_floor > current_floor:
                    self.elevator.direction = 'up'
                    self.elevator.current_floor += 1
                elif next_floor < current_floor:
                    self.elevator.direction = 'down'
                    self.elevator.current_floor -= 1
                else:
                    requests.first().delete()
            else:
                self.elevator.direction = 'stopped'
            self.elevator.save()
            time.sleep(5)

class Command(BaseCommand):
    help = 'Continuously checks the current direction of every elevator'

    def handle(self, *args, **options):
        elevators = Elevator.objects.all()
        threads = []

        for elevator in elevators:
            thread = ElevatorThread(elevator)
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()
