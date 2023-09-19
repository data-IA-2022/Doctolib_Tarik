from django.db import models
from django.contrib.auth.models import AbstractUser

class Utilisateur(AbstractUser):
  pass

# Create your models here.
# class Connexion(models.Model):
#   username = models.CharField(max_length=50)
#   mdp = models.CharField(max_length=50)