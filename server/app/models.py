from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.crypto import get_random_string

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        username = email  # Set username to email
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    email = models.EmailField(unique=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Remove 'email' from here since it's the username field

    class Meta:
        swappable = 'AUTH_USER_MODEL'

class Teacher(models.Model):
    CLASS_CHOICES = [(str(i), str(i)) for i in range(1, 11)]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    teaching_class = models.CharField(max_length=2, choices=CLASS_CHOICES)

class Student(models.Model):
    CLASS_CHOICES = [(str(i), str(i)) for i in range(1, 11)]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=10, unique=True)
    full_name = models.CharField(max_length=100)
    parents_email = models.EmailField()
    student_class = models.CharField(max_length=2, choices=CLASS_CHOICES)
    parents_phone_number = models.CharField(max_length=15)

    def save(self, *args, **kwargs):
        if not self.student_id:
            self.student_id = get_random_string(8).upper()
        super().save(*args, **kwargs)