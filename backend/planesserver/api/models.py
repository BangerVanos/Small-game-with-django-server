from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from .managers import PlanesUserManager


# Create your models here.
class PlanesUser(AbstractBaseUser, PermissionsMixin):
    """Custom user model. When authenticated, use your nickname"""
    username = models.CharField(unique=True, max_length=50, null=False)
    email = models.EmailField(unique=True, null=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    join_date = models.DateTimeField(default=timezone.now)

    objects = PlanesUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return f'PlanesUser(username={self.username}, email={self.email})'


class Balance(models.Model):
    """User's balance model"""
    user = models.OneToOneField(PlanesUser, on_delete=models.CASCADE)
    balance = models.FloatField(default=0)

    @property
    def get_balance(self):
        return self.balance

    def set_balance(self, value: float | int):
        if not isinstance(value, float) and not isinstance(value, int):
            raise ValueError('Balance can only be numeric type!')
        self.balance = value

    def add(self, value: float | int):
        if not isinstance(value, float) and not isinstance(value, int):
            raise ValueError('Balance can only be manipulated with numeric types (float, int)!')
        if value < 0:
            raise ValueError('Do no try to add negative number! Use \'subtract\' method instead!')
        self._manipulate_balance(value)

    def subtract(self, value: float | int):
        if not isinstance(value, float) and not isinstance(value, int):
            raise ValueError('Balance can only be manipulated with numeric types (float, int)!')
        if value < 0:
            raise ValueError('Do no try to subtract negative number! Use \'subtract\' method instead!')
        if value > self.balance:
            raise ValueError('Do not try to subtract more than you have on your balance!')
        self._manipulate_balance(-value)

    def _manipulate_balance(self, value: float | int):
        if not isinstance(value, float) and not isinstance(value, int):
            raise ValueError('Balance can only be manipulated with numeric types (float, int)!')
        self.balance += value
        self.save()

    def __str__(self):
        return f'{self.user.username}\'s profile'


class OpenedItems(models.Model):
    item_id = models.TextField(null=False)
    user = models.ForeignKey(PlanesUser, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.item_id}. Opened by {self.user.username}.'
