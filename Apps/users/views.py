from rest_framework import viewsets
from .serializers import PayMethodSerializer, GerenteSerializer, OperatorSerializer, ProviderSerializer, PointSerializer, WorkDaySerializer, BatidaSerializer
from .models import PayMethod, Gerente, Operator, Provider, Point, WorkDay, Batida
from .permissions import IsRoleUser
from rest_framework import permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

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
    permission_classes = [permissions.AllowAny]
    lookup_field = 'id'

    def list_batidas_of_point(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            batidas = Batida.objects.filter(point=instance)

            serializer = BatidaSerializer(batidas, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
class BatidaViewSet(viewsets.ModelViewSet):
    """
    
    """
    queryset = Batida.objects.all()
    serializer_class = BatidaSerializer
    lookup_field = 'id'

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        data_response = {}
        if serializer.is_valid():
            #verificar se o ponto é valido
            point = serializer.validated_data['point']
            time = serializer.validated_data['time']
            workday = WorkDay.objects.get(employee=point.employee, day=point.day.weekday())
            work_hours_initial = workday.work_hours_initial
            work_hours_final = workday.work_hours_final

            # Verificar se o ponto já foi fechado
            if not point.is_closed:
                # Verificar se a batida é de entrada ou saída
                if not point.batida_entry:
                    # verificando se o horario de entrada é valido
                    if time < work_hours_initial:
                        return Response({'error': 'O horário de entrada não pode ser menor que o horário de trabalho'}, status=status.HTTP_400_BAD_REQUEST)
                    point.batida_entry = True
                    type_batida = 'E'
                    point.save()
                    # verificando com o horario de trabalho de entrada
                    # aplicando a tolerancia de 15 minutos
                    work_hours_initial = work_hours_initial.replace(minute=work_hours_initial.minute + 15)
                    if time > work_hours_initial:
                        data_response['alert'] = 'Ponto com horario acima do toleravel! Comparecer ao departamento pessoal para informar o motivo do atraso!'
                    
                elif not point.batida_exit:
                    # verificar se a batida de saida é no minimo 4 horas depois da entrada
                    time_worked = time.hour - work_hours_initial.hour
                    if time_worked < 4:
                        return Response({'error': 'O horário de saída não pode ser menor que 4 horas após a entrada'}, status=status.HTTP_400_BAD_REQUEST)
                    # verificar se a batida de saida é maior que a de entrada
                    time_batida_entry = Batida.objects.get(point=point, type_batida='E').time
                    if time_batida_entry > time:
                        return Response({'error': 'A batida de saida não pode ser menor que a de entrada'}, status=status.HTTP_400_BAD_REQUEST)
                    point.batida_exit = True
                    type_batida = 'S'
                    point.is_closed = True
                    point.save()
                    print(f'tiem: {time}')
                    print(f'work_hours_final: {work_hours_final}')
                    print(time < work_hours_final)
                    # verificar com o horario de trabalho de saida
                    if time < work_hours_final:
                        data_response['alert'] = 'Ponto com horario abaixo do toleravel! Comparecer ao departamento pessoal para informar o motivo da saida antecipada!'
                    # adicionando um dia de trabalho para o funcionario
                    employee = point.employee
                    employee.days_worked += 1
                    employee.save()
                        
                Batida.objects.create(
                    point=point,
                    type_batida=type_batida,  # Definir o valor de type_batida
                    time=time,
                )

                # Calcular hora trabalhada e realizar o incremento
                if point.is_closed:    
                    batidas = Batida.objects.filter(point=point)
                    time_worked = batidas[1].time.hour - batidas[0].time.hour
                    employee = point.employee
                    employee.hours_worked += time_worked
                    employee.save()

                return Response({'message': 'Batida realizada com sucesso', **data_response}, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'Ponto já fechado'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
class WorkDayViewSet(viewsets.ModelViewSet):
    """
    
    """
    queryset = WorkDay.objects.all()
    serializer_class = WorkDaySerializer
    lookup_field = 'id'

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
        
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
