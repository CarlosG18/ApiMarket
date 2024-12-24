from rest_framework import viewsets
from .serializers import PayMethodSerializer, GerenteSerializer, OperatorSerializer, ProviderSerializer, PointSerializer, WorkDaySerializer
from .models import PayMethod, Gerente, Operator, Provider, Point, WorkDay

# Create your views here.
class PayMethodViewSet(viewsets.ModelViewSet):
    """
    
    """
    queryset = PayMethod.objects.all()
    serializer_class = PayMethodSerializer

class GerenteViewSet(viewsets.ModelViewSet):
    """
    
    """
    queryset = Gerente.objects.all()
    serializer_class = GerenteSerializer

class OperatorViewSet(viewsets.ModelViewSet):
    """
    
    """
    queryset = Operator.objects.all()
    serializer_class = OperatorSerializer

class ProviderViewSet(viewsets.ModelViewSet):
    """
    
    """
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer

class PointViewSet(viewsets.ModelViewSet):
    """
    
    """
    queryset = Point.objects.all()
    serializer_class = PointSerializer

class WorkDayViewSet(viewsets.ModelViewSet):
    """
    
    """
    queryset = WorkDay.objects.all()
    serializer_class = WorkDaySerializer