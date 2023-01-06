from django.contrib import admin
from .models import PokemonEntity, Pokemon


admin.site.register(Pokemon)
admin.site.register(PokemonEntity)
