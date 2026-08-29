from django.contrib import admin
from .models import Guest

@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    list_display = ('name', 'name_companions', 'phone', 'is_attending', 'created_at')
    list_filter = ('name', 'is_attending')
