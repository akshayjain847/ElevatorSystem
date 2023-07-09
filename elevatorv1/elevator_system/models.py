from django.db import models

class Elevator(models.Model):
    STATUS_CHOICES = [
        ('running', 'Running'),
        ('stopped', 'Stopped'),
        ('maintenance', 'Maintenance'),
    ]

    DIRECTION_CHOICES = [
        ('up', 'Up'),
        ('down', 'Down'),
        ('stopped', 'Stopped'),
    ]

    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default='stopped')
    current_floor = models.IntegerField(default=1)
    direction = models.CharField(max_length=10, choices=DIRECTION_CHOICES, default='stopped')
    requests = models.ManyToManyField('Request', related_name='elevators')
    elevator_id = models.AutoField(primary_key=True)

    def move_up(self):
        self.current_floor += 1
        self.direction = 'up'
        self.save()

    def move_down(self):
        self.current_floor -= 1
        self.direction = 'down'
        self.save()

    def stop(self):
        self.direction = 'stopped'
        self.save()

    def open_door(self):
        # Implementation for opening the door
        pass

    def close_door(self):
        # Implementation for closing the door
        pass

    @classmethod
    def initialize_system(cls, num_elevators):
        elevators = []
        for _ in range(num_elevators):
            elevator = cls.objects.create()
            elevators.append(elevator)
        return elevators

    def __str__(self):
        return f"Elevator {self.elevator_id}"


class Request(models.Model):
    floor = models.IntegerField()
    elevator_id = models.IntegerField()

    def __str__(self):
        return f"Request {self.elevator_id}"
