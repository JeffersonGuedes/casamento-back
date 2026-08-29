from django.contrib import admin
from .models import Gift

@admin.register(Gift)
class GiftAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'link', 'status', 'buyer_name')
    list_filter = ('status', 'category')
