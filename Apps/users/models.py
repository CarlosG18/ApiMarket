from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone

# Create your models here.
class Role(models.Model):
    nome = models.CharField(max_length=50)
    descricao = models.CharField(max_length=300)

    def __str__(self):
        return self.nome
    
class UserManager(BaseUserManager):
    def create_user(self, username, email, password, is_staff, is_superuser, **extra_fields):
        now = timezone.now()
        if not username:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, is_staff=is_staff, is_active=True, is_superuser=is_superuser, last_login=now, date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, username, email=None, password=None, **extra_fields):
        return self._create_user(username, email, password, False, False, **extra_fields)
    
    def create_superuser(self, username, email, password, **extra_fields):
        user=self._create_user(username, email, password, True, True, **extra_fields)
        user.is_active=True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    """
        criando um usuario customizado para a API
    """    
    first_name = models.CharField('first name', max_length=30)
    last_name = models.CharField('last name', max_length=30)
    email = models.EmailField('email address', max_length=255, unique=True)
    is_staff = models.BooleanField('staff status', default=False, help_text='Designates whether the user can log into this admin site.')
    is_active = models.BooleanField('active', default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.')
    date_joined = models.DateTimeField('date joined', default=timezone.now)
    roles = models.ManyToManyField(Role, related_name='user')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = UserManager()

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        
    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()
    
    def get_short_name(self):
        return self.first_name
    
class Employee(models.Model):
    """
        Basic model for types of employee
    """ 
    salario = models.DecimalField(max_digits=10, decimal_places=2)
    hours_worked = models.DecimalField(max_digits=10, decimal_places=2)
    days_worked = models.IntegerField(default=0)

class WorkDay(models.Model):
    """
        Basic model for work days
    """
    CHOICE_DAYS = {
        1: "domingo",
        2: "segunda",
        3: "terça",
        4: "quarta",
        5: "quinta",
        6: "sexta",
        7: "sabado",
    }

    day = models.IntegerField(choices=CHOICE_DAYS)
    work_hours_initial = models.TimeField()
    work_hours_final = models.TimeField()
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='workdays')

class PayMethod(models.Model):
    """
        model for create the pay method used for provider
    """
    name = models.CharField(max_length=200)
    is_digital = models.BooleanField(default=False)

    def __str__(self):
        return super().__str__()

class Provider(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='provider_user')
    cnpj = models.CharField(max_length=14)
    paymethod = models.ForeignKey(PayMethod, on_delete=models.CASCADE)

class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='admin_user')

class Gerente(Employee):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='gerente_user')

class Operator(Employee):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='operador_user')

class Client(models.Model):
    name = models.CharField(max_length=200)
    cpf = models.CharField(max_length=11)
    endereco = models.CharField(max_length=300)
    telefone = models.CharField(max_length=50)

class Point(models.Model):
    """
        model for create the point of the employee
    """
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='employee')
    day = models.DateField()
    batida_entry = models.BooleanField(default=False)
    batida_exit = models.BooleanField(default=False)
    is_closed = models.BooleanField(default=False)

class Batida(models.Model):
    TYPE_CHOICE = (
        ('E', 'Entrada'),
        ('S', 'Saida'),
    )

    time = models.TimeField()
    type_batida = models.CharField(max_length=1, choices=TYPE_CHOICE, default='E')
    point = models.ForeignKey('Point', on_delete=models.CASCADE)