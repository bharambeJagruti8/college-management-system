from django.contrib import admin
from django.contrib import admin
from .models import BonafideRequest

@admin.register(BonafideRequest)
class BonafideRequestAdmin(admin.ModelAdmin):
    list_display = ['student', 'purpose', 'addressed_to', 'status', 'created_at']
    list_filter = ['status', 'purpose']
    list_editable = ['status']
    search_fields = ['student__username', 'addressed_to']
# Register your models here.
