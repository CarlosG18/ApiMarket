from rest_framework import viewsets
from .serializers import PayMethodSerializer, GerenteSerializer, OperatorSerializer, ProviderSerializer, PointSerializer, WorkDaySerializer, BatidaSerializer
from .models import PayMethod, Gerente, Operator, Provider, Point, WorkDay, Batida
from .permissions import IsRoleUser
from rest_framework import permissions, status
from rest_framework.response import Response

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
        ViewSet for the Point model. apenas Gerente e Operator podem acessar pois são os unicos fucnionarios
    """
    queryset = Point.objects.all()
    serializer_class = PointSerializer
    #requer_roles = ['Gerente', 'Operator']
    #permission_classes = [IsRoleUser]
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """
            para o funcionario criar um ponto ele deve ter cadastrado as suas workdays
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            #verificar se o dia atual é um dia de trabalho
            employee = serializer.validated_data['employee']
            workdays = WorkDay.objects.filter(employee=employee)
            
            days_of_work = [workday.day for workday in workdays]
            today = serializer.validated_data['day']
            today_day = today.weekday()
            if today_day not in days_of_work:
                return Response({'error': 'Você não possui horarios de trabalhos para esse dia!'}, status=status.HTTP_400_BAD_REQUEST)
            
            super().create(request, *args, **kwargs)
            return Response({'message': 'Ponto criado com sucesso'}, status=status.HTTP_201_CREATED)
            
class BatidaViewSet(viewsets.ModelViewSet):
    """
    
    """
    queryset = Batida.objects.all()
    serializer_class = BatidaSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            #verificar se o ponto é valido
            point = serializer.validated_data['point']
            time = serializer.validated_data['time']

            # Verificar se o ponto já foi fechado
            if not point.is_closed:
                # Verificar se a batida é de entrada ou saída
                if not point.batida_entry:
                    point.batida_entry = True
                    type_batida = 'E'
                    point.save()

                if point.batida_entry and not point.batida_exit:
                    point.batida_exit = True
                    type_batida = 'S'
                    point.is_closed = True
                    point.save()

                # verificar se o horario da batida é valido
                if not point.is_valid_time(time):
                    return Response({'error': 'Horario de batida inválido'}, status=status.HTTP_400_BAD_REQUEST)

                # Criar o objeto Batida
                Batida.objects.create(
                    point=point,
                    type_batida=type_batida,  # Definir o valor de type_batida
                    time=time,
                )
                return Response({'message': f'Batida de {type_batida} criada com sucesso'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'Ponto já fechado'}, status=status.HTTP_400_BAD_REQUEST)
            
class WorkDayViewSet(viewsets.ModelViewSet):
    """
    
    """
    queryset = WorkDay.objects.all()
    serializer_class = WorkDaySerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Verificar se o dia de trabalho já existe
            employee = serializer.validated_data['employee']
            day = serializer.validated_data['day']
            workday = WorkDay.objects.filter(employee=employee, day=day)
            if workday.exists():
                return Response({'error': 'Dia de trabalho já cadastrado'}, status=status.HTTP_400_BAD_REQUEST)
            
            self.perform_create(serializer)
            return Response({'message': 'Dia de trabalho cadastrado com sucesso'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)