from django.contrib import admin
from django.utils.html import format_html
from accounts.models import Participant, Zone, ZoneCaptain, ParticipantGroup, Application
from .models import IndividualItem, GroupItem

admin.site.register(Zone)
admin.site.register(IndividualItem)
admin.site.register(GroupItem)

class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('photo_display', 'name', 'email', 'zone', 'studentid')
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

    def photo_display(self, obj):
        return format_html('<img src="{}" width="50" height="50" style="border-radius:5px;" />', obj.photo.url)

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
admin.site.register(ParticipantGroup)
