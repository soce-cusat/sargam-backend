from django.db import models
from django.utils import timezone


ITEM_TYPE_CHOICES = [
    ("Group", "Group"),
    ("Individual", "Individual"),
]
class ModelManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted=False)

    def all(self):
        return self.get_queryset()

    def deleted(self):
        return super().get_queryset().filter(deleted=True)


class Model(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted = models.BooleanField(default=False)
    objects = ModelManager()

    class Meta:
        abstract = True

    def delete(self, *args, **kwargs):
        self.deleted = True
        self.deleted_at = timezone.now()
        self.save()
        return self

    def hard_delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        return self


class Item(models.Model):
    item_name = models.CharField(max_length=255)
    item_type = models.CharField(max_length=255,choices=ITEM_TYPE_CHOICES,default="Individual")

    def __str__(self):
        return str(self.item_name)

class GroupItem(models.Model):
    item_name = models.CharField(max_length=255)
    # first = models.ForeignKey("accounts.ParticipantGroup", on_delete=models.CASCADE, related_name="first_place_results", null=True)
    # second = models.ForeignKey("accounts.ParticipantGroup", on_delete=models.CASCADE, related_name="second_place_results", null=True)
    # third = models.ForeignKey("accounts.ParticipantGroup", on_delete=models.CASCADE, related_name="third_place_results", null=True)

    def __str__(self):
        return self.item_name
    

