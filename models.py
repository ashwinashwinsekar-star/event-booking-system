from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email address is required')
        email = self.normalize_email(email)
        username = extra_fields.get('username') or email.split('@')[0]
        extra_fields['username'] = username
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'Admin')
        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    ROLE_CHOICES = (
        ('Attendee', 'Attendee'),
        ('Organizer', 'Organizer'),
        ('Admin', 'Admin'),
    )

    email = models.EmailField(unique=True)
    name = models.CharField(max_length=150, blank=True)
    phone = models.CharField(max_length=25, blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Attendee')
    created_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'name']

    def __str__(self):
        return f"{self.name or self.username} ({self.email}) - {self.role}"

    @property
    def is_organizer(self):
        return self.role in ['Organizer', 'Admin'] or self.is_staff

    @property
    def is_admin(self):
        return self.role == 'Admin' or self.is_superuser
