from django.contrib import admin
from django.urls import path

from pokemon_entities import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.all_pokemons_map, name="mainpage"),
    path('pokemon/<slug:slug>/', views.show_pokemon, name="pokemon"),
]
