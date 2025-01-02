from .models import Gerente, Operator, Provider, Point, WorkDay, PayMethod, Role, Admin, User, Employee, Batida, Client
from rest_framework import serializers
from django.utils import timezone
from datetime import datetime
import re

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'nome', 'descricao']
class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'

class BatidaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Batida
        fields = ['id', 'point', 'type_batida', 'time']
        read_only_fields = ['type_batida']

class ProviderSerializer(serializers.ModelSerializer):
    roles = RoleSerializer(many=True, read_only=True)
    first_name = serializers.CharField(source='user.first_name', required=True)
    last_name = serializers.CharField(source='user.last_name', required=True)
    email = serializers.EmailField(source='user.email', required=True)
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Provider
        fields = [
            'id', 'first_name', 'last_name', 'email', 'password', 'roles', 'cnpj', 'paymethod'
        ]
        read_only_fields = ['id']

    def validate_email(self, value):
        """Ensure the email is unique among Admins."""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value

    def create(self, validated_data):
        """Create a new Admin instance with a related User."""
        user_data = validated_data.pop('user')  # Dados vindos do source='user.*'
        password = validated_data.pop('password')  # Campo diretamente no serializer

        # Crie o objeto User
        user = User.objects.create(
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            email=user_data['email'],
        )
        user.set_password(password)
        user.save()
            
        provider = Provider.objects.create(user=user, **validated_data)

        role, created = Role.objects.get_or_create(nome='Provider', defaults={'descricao': 'Provider role'})
        user.roles.add(role)
        
        return provider

class PayMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayMethod
        fields = '__all__'

class PointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Point
        fields = ['id', 'employee', 'day', 'is_closed']
        read_only_fields = ['is_closed']

    def validate_day(self, value):
        # verificar se o dia não está no passado ou no futuro    
        if value < datetime.now().date():
            raise serializers.ValidationError("O dia não pode ser no passado.")
        #if value > timezone.now().date():
           #raise serializers.ValidationError("O dia não pode ser no futuro.")
        
        # verificar se não existe um ponto para o dia
        if Point.objects.filter(day=value).exists():
            raise serializers.ValidationError("Já existe um ponto para este dia.")
        
        return value

class WorkDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkDay
        fields = '__all__'

    def validate(self, attrs):
        # verificar se o horario de trabalho é valido
        work_hours_initial = attrs['work_hours_initial']
        work_hours_final = attrs['work_hours_final']

        # Verificar se os horários são válidos
        if work_hours_initial >= work_hours_final:
            raise serializers.ValidationError("O horário inicial deve ser menor que o horário final.")
        
        # Calcular a duração da jornada de trabalho
        hours_total_initial = work_hours_initial.hour + work_hours_initial.minute / 60
        hours_total_final = work_hours_final.hour + work_hours_final.minute / 60

        jornada_trabalho = hours_total_final - hours_total_initial

        if jornada_trabalho > 8.0:
            raise serializers.ValidationError("A jornada de trabalho não pode exceder 8 horas.")
        if jornada_trabalho < 4.0:
            raise serializers.ValidationError("A jornada de trabalho deve ter no mínimo 4 horas.")

        return attrs

class AdminSerializer(serializers.ModelSerializer):
    roles = RoleSerializer(many=True, read_only=True)
    first_name = serializers.CharField(source='user.first_name', required=True)
    last_name = serializers.CharField(source='user.last_name', required=True)
    email = serializers.EmailField(source='user.email', required=True)
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Admin
        fields = [
            'id', 'first_name', 'last_name', 'email', 'password', 'roles'
        ]
        read_only_fields = ['id']

    def validate_email(self, value):
        """Ensure the email is unique among Admins."""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value

    def create(self, validated_data):
        """Create a new Admin instance with a related User."""
        user_data = {
            'first_name': validated_data["user"].pop('first_name'),
            'last_name': validated_data["user"].pop('last_name'),
            'email': validated_data["user"].pop('email'),
            'password': validated_data.pop('password')
        }
        
        user = User.objects.create(**user_data)
        user.set_password(user_data['password'])
        
        admin = Admin.objects.create(user=user, **validated_data["user"])

        role, created = Role.objects.get_or_create(nome='Admin', defaults={'descricao': 'Admin role'})
        user.roles.add(role)

        user.save()
        admin.save()
        
        return admin

class GerenteSerializer(serializers.ModelSerializer):
    roles = RoleSerializer(many=True, read_only=True)
    first_name = serializers.CharField(source='user.first_name', required=True)
    last_name = serializers.CharField(source='user.last_name', required=True)
    email = serializers.EmailField(source='user.email', required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate_email(self, value):
        """Ensure the email is unique among Users."""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value

    def create(self, validated_data):
        # Dados do User
        user_data = validated_data.pop('user')
        user_data['password'] = validated_data.pop('password')
        user = User.objects.create(**user_data)
        user.set_password(user_data['password'])
        user.save()

        # Crie Gerente
        gerente = Gerente.objects.create(user=user, **validated_data)

        # Atribua o papel de Gerente
        role, created = Role.objects.get_or_create(
            nome='Gerente', defaults={'descricao': 'Gerente role'}
        )
        user.roles.add(role)
        gerente.save()

        return gerente

    class Meta:
        model = Gerente
        fields = [
            'id', 'first_name', 'last_name', 'email', 'password', 'roles', 'salario', 'hours_worked'
        ]
        read_only_fields = ['id']

class OperatorSerializer(serializers.ModelSerializer):
    roles = RoleSerializer(many=True, read_only=True)
    first_name = serializers.CharField(source='user.first_name', required=True)
    last_name = serializers.CharField(source='user.last_name', required=True)
    email = serializers.EmailField(source='user.email', required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate_email(self, value):
        """Ensure the email is unique among Editores."""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value

    def create(self, validated_data):
        # Dados do User
        user_data = validated_data.pop('user')
        user_data['password'] = validated_data.pop('password')
        user = User.objects.create(**user_data)
        user.set_password(user_data['password'])
        user.save()

        # Crie Gerente
        operator = Operator.objects.create(user=user, **validated_data)

        # Atribua o papel de Gerente
        role, created = Role.objects.get_or_create(
            nome='operator', defaults={'descricao': 'Operator role'}
        )
        user.roles.add(role)
        operator.save()

        return operator

    class Meta:
        model = Operator
        fields = [
            'id', 'first_name', 'last_name', 'email', 'password', 'roles', 'salario', 'hours_worked'
        ]
        read_only_fields = ['id']