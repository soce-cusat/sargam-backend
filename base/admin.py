from django.contrib import admin
from django.utils.html import format_html

from accounts.models import Participant, Zone, ZoneCaptain
from .models import IndividualItem, GroupItem, ParticipantGroup

admin.site.register(Zone)
admin.site.register(IndividualItem)
admin.site.register(ParticipantGroup)
admin.site.register(GroupItem)

class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('photo_display', 'name', 'email', 'zone', 'studentid', 'is_verified')
    search_fields = ('name', 'email', 'studentid')
    list_filter = ('zone',)
    ordering = ('name',)

    fieldsets = (
        (None, {
            'fields': ('is_verified_display', 'name', 'zone', 'items', 'studentid')}),
        ('Additional Info', {'fields': ('user', 'email', 'photo')}),
    )

    readonly_fields = ('is_verified_display',)
    
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

@admin.register(ZoneCaptain)
class ZoneCaptainAdmin(admin.ModelAdmin):
    exclude = ("user",)

admin.site.register(Participant, ParticipantAdmin)
