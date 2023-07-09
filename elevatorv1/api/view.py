from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view(['GET'])
def getData(request):
    elevator_start = {'name' : 'elevator1' , 'function' : 'start'}
    return Response(elevator_start)