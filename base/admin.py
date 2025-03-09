from django.contrib import admin
from django.utils.html import format_html
from accounts.models import Participant, Zone, ZoneCaptain, ParticipantGroup, Application
from .models import Item, GroupItem

admin.site.register(Zone)

class ItemAdmin(admin.ModelAdmin):
    search_fields = ['item_name']  # Enables search by item_name


admin.site.register(Item, ItemAdmin)
# admin.site.register(GroupItem, GroupItemAdmin)

class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('photo_display', 'name', 'email', 'ph_number', 'zone', 'studentid')
    search_fields = ('name', 'email', 'studentid')
    list_filter = ('zone',)
    ordering = ('name',)

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
        return format_html('<img src="{}" width="50" height="50" style="border-radius:3px;" />', obj.photo.url)
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
    list_display = [ 'item__item_name', 'status']
    search_fields = [ 'item__item_name']
    list_editable = ['status']

    def item__item_name(self, obj):
        return obj.item.item_name
    item__item_name.short_description = "Item"

    def get_list_filter(self, request):
        if request.user.is_superuser:
            return ['participant', 'participant__zone']
        else:
            return ['participant']
    
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
