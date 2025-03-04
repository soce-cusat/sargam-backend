from django.db import models
from config.settings.base import AUTH_USER_MODEL
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.apps import apps

User = get_user_model()
codenames = ['delete_participant', 'view_participant', 'change_participant', 'add_participant']

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
	user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True, )
	name = models.CharField(max_length=50)
	password = models.CharField(max_length=50)
	email = models.EmailField(max_length=254)
	zone = models.ForeignKey(Zone, on_delete=models.CASCADE)
	
	def save(self, *args, **kwargs):
		new_user = User.objects.create_user(
				full_name=self.name,
				email=self.email, 
				password=self.password,
				is_staff=True
		)
		group, created = Group.objects.get_or_create(name='ZoneCaptains')
		if created:
			ct = ContentType.objects.get_for_model(Participant)
			permissions = Permission.objects.filter(content_type=ct, codename__in=codenames)		
			for permission in permissions.all():
				group.permissions.add(permission)
		group.user_set.add(new_user)
		new_user.save()
		self.user = new_user
		return super().save(*args, **kwargs)

	def delete(self, *args, **kwargs):
		self.user.delete()
		super().delete(*args, **kwargs) 

	def __str__(self):
 		return self.name + " - " + self.zone.name