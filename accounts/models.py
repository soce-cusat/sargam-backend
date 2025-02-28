from enum import unique
from django.db import models
from django.contrib.auth.models import User
from django.utils.http import unicodedata
from config.settings.base import AUTH_USER_MODEL

class Zone(models.Model):
	name = models.CharField(max_length=50)
	
	def __str__(self):
 		return self.name


class Participant(models.Model):
	user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
	name = models.CharField(max_length=50, blank=False, null=False)
	email = models.EmailField(unique=True)
	zone = models.ForeignKey(Zone, on_delete=models.CASCADE)
	photo = models.ImageField()

	def __str__(self):
 		return self.user.get_full_name()
