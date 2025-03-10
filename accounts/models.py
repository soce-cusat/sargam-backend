from django.db import models
from config.settings.base import AUTH_USER_MODEL
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.files.base import ContentFile
from base.models import Item
from PIL import Image
from io import BytesIO

User = get_user_model()
codenames = ['delete_participant', 'view_participant', 'change_participant', 'add_participant'
			 ,'delete_application', 'view_application', 'change_application', 'add_application']

class Zone(models.Model):
	name = models.CharField(max_length=50)
	
	def __str__(self):
 		return self.name


class Participant(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, blank=False, null=False)
    email = models.EmailField(unique=True)
    ph_number = models.CharField(max_length=10, blank=False, null=False, default=0)
    zone = models.ForeignKey("Zone", on_delete=models.CASCADE)
    photo = models.ImageField()
    studentid = models.IntegerField(unique=True)
    id_card = models.ImageField(null=True, blank=True)
    verified = models.BooleanField(default=False)

    def compress_image(self, image_field):
        img = Image.open(image_field)
        img = img.convert('RGB')
        img.thumbnail((800, 800))
        buffer = BytesIO()
        img.save(buffer, format="JPEG", quality=70)  
        return ContentFile(buffer.getvalue(), name=image_field.name)

    def save(self, *args, **kwargs):
        if self.photo:
            self.photo = self.compress_image(self.photo)
        if self.id_card:
            self.id_card = self.compress_image(self.id_card)
        super().save(*args, **kwargs)

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
	
class ParticipantGroup(models.Model):
	name = models.CharField(max_length=50, default="Group name", null=False, blank=False)
	zone = models.ForeignKey(Zone, on_delete=models.CASCADE)
	participants = models.ManyToManyField(Participant, related_name="group")
	item = models.ForeignKey('base.Item', on_delete=models.CASCADE)

	def __str__(self):
		return self.item.name + " - " + self.zone.name
	

class Application(models.Model):
    PENDING = 'pending'
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (ACCEPTED, 'Accepted'),
        (REJECTED, 'Rejected'),
    ]

    participant = models.ForeignKey('Participant', on_delete=models.CASCADE)
    item = models.ForeignKey(Item,on_delete=models.CASCADE)  # Changed to ManyToManyField
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)
	
    def __str__(self):
	    return self.participant.name + ' - ' + self.item.item_name 