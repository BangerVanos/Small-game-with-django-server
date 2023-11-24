from django.contrib.auth.models import BaseUserManager


class PlanesUserManager(BaseUserManager):

    use_in_migrations = True

    def create_user(self, username: str, email: str, password: str = None, **extra_fields):
        extra_fields.setdefault('is_active', True)
        if not username:
            raise ValueError('Nickname is required field')
        if not email:
            raise ValueError('Email is required field')
        if extra_fields.get('is_active') is not True:
            raise ValueError('When creating new user, \'is_active\' must be True')
        email = self.normalize_email(email=email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username: str, email: str, password: str = None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('For superuser \'is_staff\' must be True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('For superuser \'is_superuser\' must be True')
        return self.create_user(username=username, email=email, password=password, **extra_fields)

