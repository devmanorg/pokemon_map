from django.contrib import admin
from .models import Pokemon

@admin.register(Pokemon)
class Pokemon(admin.ModelAdmin):
    list_display = ('title', 'image')

