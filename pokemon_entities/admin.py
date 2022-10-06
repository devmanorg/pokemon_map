from django.contrib import admin
from .models import Pokemon, PokemonEntity

@admin.register(Pokemon)
class Pokemon(admin.ModelAdmin):
    list_display = ('pokemon_id', 'title', 'image', 'description')


@admin.register(PokemonEntity)
class PokemonEntity(admin.ModelAdmin):
    list_display = ('pokemon', 'latitude', 'longitude')

