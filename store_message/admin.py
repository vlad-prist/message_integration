from django.contrib import admin
from store_message.models import Store


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('theme', 'description', 'date_sanding', 'date_receiving', 'owner',)
    search_fields = ('theme', 'date_sanding', 'date_receiving',)
    list_filter = ('theme',)

