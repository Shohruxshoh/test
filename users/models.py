from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    phone = models.CharField(max_length=15, unique=True, null=True, blank=True)

    def __str__(self):
        return self.username
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)  # Tug'ilgan sana
    bio = models.TextField(blank=True, null=True)  # Foydalanuvchi haqida qisqacha ma'lumot
    website = models.URLField(blank=True, null=True)  # Shaxsiy veb-sayt yoki blog manzili

    def __str__(self):
        return f"Profil: {self.user.username}"
