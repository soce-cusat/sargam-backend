from django.db import models
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
	studentid = models.IntegerField(unique=True)
	id_card = models.ImageField(null=True, blank=True)
	items = models.ManyToManyField('base.IndividualItem', related_name="participant", blank=True)

	def __str__(self):
 		return self.user.get_full_name()

class ZoneCaptain(models.Model):
	user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
	name = models.CharField(max_length=50)
	zone = models.ForeignKey(Zone, on_delete=models.CASCADE)

	def __str__(self):
 		return self.name + " - " + self.zone.name