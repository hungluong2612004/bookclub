from django.contrib import admin

from . models import ShelfItem, ShelfOption

# Register your models here.

admin.site.register(ShelfItem)

class ShelfOptionAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('shelf_option', )}

admin.site.register(ShelfOption, ShelfOptionAdmin)
