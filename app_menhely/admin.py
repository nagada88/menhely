from django.contrib import admin
from .models import *
from parler.admin import TranslatableAdmin

class PictureInline(admin.StackedInline):
    model = AllatImage
    
class MainPictureInline(admin.StackedInline):
    model = AllatMainImage

    def get_extra(self, request, obj=None, **kwargs):
        if obj:
            return 0 # For changing an item
        else: 
            return 1 # For adding a new item

class AllatAdmin(admin.ModelAdmin):
    inlines = [MainPictureInline, PictureInline]

# Register your models here.
admin.site.register(Allat, AllatAdmin)
admin.site.register(Bemutatkozas, TranslatableAdmin)
admin.site.register(Hirek, TranslatableAdmin)
admin.site.register(Kapcsolat, TranslatableAdmin)
admin.site.register(Kimutatasok)

