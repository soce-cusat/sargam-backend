from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils.html import format_html
from .models import Participant

@admin.action(description="Add selected participants to Zone Captains")
def add_participants_to_group(modeladmin, request, queryset):
    group_name = "Zone Captains"  # Change this to your desired group
    group, created = Group.objects.get_or_create(name=group_name)

    for participant in queryset:
        participant.user.groups.add(group)  # Assuming your model is linked to User

    modeladmin.message_user(request, f"Selected participants added to {group_name} group.")

@admin.action(description="Remove selected participants from Zone Captains")
def remove_participants_from_group(modeladmin, request, queryset):
    group_name = "Zone Captains"  # Change this to your desired group
    group = Group.objects.get(name=group_name)

    for participant in queryset:
        participant.user.groups.remove(group)  # Assuming your model is linked to User

    modeladmin.message_user(request, f"Selected participants removed from {group_name} group.")

class ParticipantAdmin(admin.ModelAdmin):
    list_display = ("photo_tag", "name", "email", "zone", "studentid","id_card","user")
    search_fields = ("name", "email", "zone__name")

    actions = [add_participants_to_group, remove_participants_from_group]  # Add custom actions here

    def photo_tag(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="width: 100px; height:180px;" />'.format(obj.photo.url))
        return "-"
    photo_tag.short_description = 'Photo'

    def id_card(self, obj):
        if obj.id_card:
            return format_html('<img src="{}" style="width: 100px; height:180px;" />'.format(obj.id_card.url))
        return "-"
    id_card.short_description = 'ID Card'

# Unregister the existing Participant model
admin.site.unregister(Participant)

# Register the Participant model with the custom actions
admin.site.register(Participant, ParticipantAdmin)
