import folium
import json

from django.http import Http404
from django.shortcuts import render
# Create your views here.


def make_pokemon_map(pokemons):
    moscow_center = [55.8738792716378000, 37.5673603455195320]
    folium_map = folium.Map(
        location=moscow_center,
        zoom_start=15,
    )
    for pokemon in pokemons:
        for pokemon_entity in pokemon['entities']:
            icon = folium.features.CustomIcon(
                pokemon['img_url'],
                icon_size=(50, 50),
            )
            folium.Marker(
                [pokemon_entity['lat'], pokemon_entity['lon']],
                tooltip=pokemon['title_ru'],
                icon=icon,
            ).add_to(folium_map)
    html_map = folium_map._repr_html_()
    return html_map


def all_pokemons_map(request):
    with open("pokemon_entities/pokemons.json") as database:
        pokemons = json.load(database)['pokemons']
    context = {
        'map': make_pokemon_map(pokemons),
        'pokemons': pokemons
    }
    return render(request, "mainpage.html", context=context)


def show_pokemon(request, title_en):
    with open("pokemon_entities/pokemons.json") as database:
        pokemons = json.load(database)['pokemons']
    for pokemon in pokemons:
        if pokemon['title_en'] == title_en:
            requested_pokemon = pokemon
            break
    else:
        raise Http404
    context = {
        'map': make_pokemon_map([pokemon]),
        'pokemon': requested_pokemon
    }
    return render(request, "pokemon.html", context=context)
