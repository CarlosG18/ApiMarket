from .models import Gerente, Operator, Provider, Point, WorkDay, PayMethod, Role, Admin, User, Employee
from rest_framework import serializers
from decimal import Decimal


class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = '__all__'

class PayMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayMethod
        fields = '__all__'

class PointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Point
        fields = '__all__'

class WorkDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkDay
        fields = '__all__'

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'nome', 'descricao']

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