from django.contrib import admin
from django.urls import path

from pokemon_entities import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.show_all_pokemons, name="mainpage"),
    path('pokemon/<pokedex_no>/', views.show_pokemon, name="pokemon"),
]
