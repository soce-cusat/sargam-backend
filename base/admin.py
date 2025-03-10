from django.contrib import admin
from django.utils.html import format_html
from accounts.models import Participant, Zone, ZoneCaptain, ParticipantGroup, Application
from .models import Item, GroupItem, Stage , Schedule
from django.contrib import admin
from django.db.models import Q

admin.site.register(Zone)
class ItemAdmin(admin.ModelAdmin):
    search_fields = ['item_name']  # Enables search by item_name
    ordering = ('item_name',)
    list_filter = ('item_type',)





admin.site.register(Item, ItemAdmin)
# admin.site.register(GroupItem, GroupItemAdmin)

class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('photo_display', 'name', 'email', 'ph_number', 'zone', 'studentid','id_card_display','verified')
    search_fields = ('name', 'email', 'studentid')
    list_filter = ('zone',)
    ordering = ('name',)
    list_editable = ('verified',)

    def get_fieldsets(self, request, obj=None):
        if request.user.is_superuser:
            return (
                (None, {'fields': ('name', 'zone', 'studentid')}),
                ('Additional Info', {'fields': ('user', 'email', 'photo', 'id_card')}),
            )
        else:
            return (
                (None, {'fields': ('name', 'studentid')}),
                ('Additional Info', {'fields': ('user', 'email', 'photo', 'id_card')}),
            )

    def ph_number(self, obj):
        return obj.ph_number
    ph_number.short_description = "Phone Number"

    def photo_display(self, obj):
        return format_html(
            '<img src="{0}" width="90" height="90" style="border-radius:3px;" />'
            '</a>',
            obj.photo.url
        )

    def id_card_display(self, obj):
        return format_html(
            '<a href="{0}" target="_blank">'
            '<img src="{0}" width="90" height="90" style="border-radius:3px;" />'
            '</a>',
            obj.id_card.url
        )

    photo_display.short_description = 'Photo'

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return ('verified',)  # Changed from 'is_verified_display' to 'verified'
        return ('email', 'studentid', 'verified')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_staff:
            zc = ZoneCaptain.objects.filter(user=request.user).first()
            if zc:
                return qs.filter(zone=zc.zone)
        return qs

@admin.register(ZoneCaptain)
class ZoneCaptainAdmin(admin.ModelAdmin):
    pass

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = [ 'participant_name','item__item_name', 'status']
    search_fields = [ 'participant_name','item__item_name']
    list_editable = ['status']

    def participant_name(self, obj) :
        return str(obj.participant.name) + " - " + str(obj.participant.studentid)

    def item__item_name(self, obj):
        return obj.item.item_name
    item__item_name.short_description = "Item"

    def get_list_filter(self, request):
        if request.user.is_superuser:
            return ['participant','item']
        else:
            return ['participant','item']
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs  # Superusers see all applications
        if request.user.is_staff:
            zc = ZoneCaptain.objects.filter(user=request.user).first()
            if zc:
                return qs.filter(participant__zone=zc.zone)
            return qs.none()  # Other staff see nothing
        return qs.none()  # Non-staff users see nothing

admin.site.register(Participant, ParticipantAdmin)
admin.site.register(Stage)


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = [ 'stage', 'item', 'start_time', 'end_time']
    search_fields = [ 'stage', 'item', 'start_time', 'end_time']
    list_filter = ('stage','item')




class ParticipantGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'zone', 'item')  # Display key fields
    search_fields = ('name', 'zone__name', 'item__name')  # Enable search
    list_filter = ('zone', 'item')  # Enable filtering by zone and item
    filter_horizontal = ('participants',)  # Allow multi-select for participants

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Filter items to include only those of type 'Group'."""
        if db_field.name == "item":
            kwargs["queryset"] = Item.objects.filter(item_type="Group")

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        """Filter participants to only include those with accepted applications."""
        if db_field.name == "participants":
            # Get participants who have an accepted application
            accepted_participant_ids = Application.objects.filter(
                status=Application.ACCEPTED
            ).values_list("participant_id", flat=True)

            kwargs["queryset"] = Participant.objects.filter(id__in=accepted_participant_ids)

        return super().formfield_for_manytomany(db_field, request, **kwargs)

# Register ParticipantGroupAdmin
admin.site.register(ParticipantGroup, ParticipantGroupAdmin)
