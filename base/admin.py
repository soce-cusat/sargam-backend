from django.contrib import admin
from django.utils.html import format_html

from accounts.models import Participant, Zone, ZoneCaptain, ParticipantGroup
from .models import IndividualItem, GroupItem

admin.site.register(Zone)
admin.site.register(IndividualItem)
admin.site.register(GroupItem)

class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('photo_display', 'name', 'email', 'zone', 'studentid', 'is_verified')
    search_fields = ('name', 'email', 'studentid')
    list_filter = ('zone',)
    ordering = ('name',)

    readonly_fields = ('is_verified_display',)
    

    def get_fieldsets(self, request, obj = None):
        if request.user.is_superuser:
            return (
        (None, {
            'fields': ('is_verified_display', 'name', 'zone', 'individual_items', 'studentid')}),
        ('Additional Info', {'fields': ('user', 'email', 'photo', 'id_card')}),)
        else:
            return (
        (None, {
            'fields': ('is_verified_display', 'name', 'individual_items', 'studentid')}),
        ('Additional Info', {'fields': ('user', 'email', 'photo', 'id_card')}),)
    
    def photo_display(self, obj):
    	return format_html('<img src="{}" width="50" height="50" style="border-radius:5px;" />', obj.photo.url)
    photo_display.short_description = 'Photo' #type: ignore

    def is_verified_display(self, obj):
        return obj.user.is_active
    is_verified_display.boolean = True
    is_verified_display.short_description = 'Verified'

    def is_verified(self, obj):
        return obj.user.is_active
    is_verified.boolean = True
    is_verified.admin_order_field = 'user__is_active'
    is_verified.short_description = 'Verified'

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return ('is_verified_display',)
        return ('email', 'studentid', 'is_verified_display')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_staff:
            zc = ZoneCaptain.objects.filter(user=request.user).first()
            if zc:
                return qs.filter(zone=zc.zone)
        return qs
    
@admin.register(ZoneCaptain)
class ZoneCaptainAdmin(admin.ModelAdmin):
    # exclude = ("user",)
    pass

admin.site.register(Participant, ParticipantAdmin)
admin.site.register(ParticipantGroup)
