from django.urls import path, include
from rest_framework import routers
from elevator_system.views import ElevatorViewSet, RequestViewSet

router = routers.DefaultRouter()
router.register(r'elevators', ElevatorViewSet)
router.register(r'requests', RequestViewSet)

urlpatterns = [
    # path('', include(router.urls)),
    path('elevators/initialize_system/', ElevatorViewSet.as_view({'post': 'initialize_system'})),
    path('elevators/<int:elevator_id>/next_destination_floor/', ElevatorViewSet.as_view({'get': 'get_next_destination_floor'})),
    path('elevators/<int:elevator_id>/direction/', ElevatorViewSet.as_view({'get': 'get_direction'})),
    path('elevators/<int:elevator_id>/add_request/', ElevatorViewSet.as_view({'post': 'add_request'})),
    path('elevators/<int:elevator_id>/mark_maintenance/', ElevatorViewSet.as_view({'post': 'mark_maintenance'})),
    path('elevators/<int:elevator_id>/open_door/', ElevatorViewSet.as_view({'post': 'open_door'})),
    path('elevators/<int:elevator_id>/close_door/', ElevatorViewSet.as_view({'post': 'close_door'})),
]
