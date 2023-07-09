from django.urls import path, include
from rest_framework import routers
from elevator_system.views import ElevatorViewSet, RequestViewSet, AddElevatorView, DeleteElevatorView, ReinitializeElevatorSystemView

router = routers.DefaultRouter()
router.register(r'elevators', ElevatorViewSet)
router.register(r'requests', RequestViewSet)

urlpatterns = [
    # path('', include(router.urls)),
    path('elevators/initialize_system/', ElevatorViewSet.as_view({'post': 'initialize_system'})),
    path('elevators/<int:elevator_id>/next_destination_floor/', ElevatorViewSet.as_view({'get': 'get_next_destination_floor'})),
    path('elevators/<int:elevator_id>/direction/', ElevatorViewSet.as_view({'get': 'get_direction'})),
    path('elevators/<int:elevator_id>/add_request/', ElevatorViewSet.as_view({'post': 'add_request_for_elevator'})),
    path('elevators/<int:elevator_id>/mark_maintenance/', ElevatorViewSet.as_view({'post': 'mark_maintenance'})),
    path('elevators/<int:elevator_id>/open_door/', ElevatorViewSet.as_view({'post': 'open_door'})),
    path('elevators/<int:elevator_id>/close_door/', ElevatorViewSet.as_view({'post': 'close_door'})),
    path('elevators/<int:floor_id>/add_new_request/', RequestViewSet.as_view({'post': 'add_request_for_floor'})),
    path('elevators/<int:elevator_id>/get_floor_list/', ElevatorViewSet.as_view({'get': 'get_all_request_of_elevator'})),
    path('elevators/<int:elevator_id>/request_floor/<int:floor_id>', ElevatorViewSet.as_view({'get': 'request_elevator_to_floor'})),
    path('elevators/add', AddElevatorView.as_view({'post': 'new_elevator'})),
    path('elevators/<elevator_id>/delete/', DeleteElevatorView.as_view({'delete': 'delete_elevator'})),
    path('elevators/reinitialise', ReinitializeElevatorSystemView.as_view({'post': 'reinitialise'})),
]
