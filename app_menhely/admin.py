from django.contrib import admin
from .models import *
from parler.admin import TranslatableAdmin

class PictureInline(admin.StackedInline):
    model = AllatImage
    
class MainPictureInline(admin.StackedInline):
    model = AllatMainImage
    
class AllatAdmin(admin.ModelAdmin):
    inlines = [PictureInline, MainPictureInline]

# Register your models here.
admin.site.register(Allat, AllatAdmin)
admin.site.register(Bemutatkozas, TranslatableAdmin)
admin.site.register(Hirek, TranslatableAdmin)
admin.site.register(Kapcsolat, TranslatableAdmin)
admin.site.register(Kimutatasok)

