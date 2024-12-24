from rest_framework import viewsets
from .models import PayMethod
from .serializers import PayMethodSerializer

# Create your views here.
# Create your views here.
class PayMethodViewSet(viewsets.ModelViewSet):
    """
    
    """
    queryset = PayMethod.objects.all()
    serializer_class = PayMethodSerializer