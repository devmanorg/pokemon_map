import folium
import json

from django.http import HttpResponseNotFound
from django.shortcuts import render


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = "https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832&fill=transparent"

def add_pokemon(folium_map, lat, lon, name, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        tooltip=name,
        icon=icon,
    ).add_to(folium_map)
    return folium_map


def show_all_pokemons(request):
    with open("pokemon_entities/pokemons.json") as database:
        pokemons = json.load(database)['pokemons']

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon in pokemons:
        for pokemon_entity in pokemon['entities']:
            folium_map = add_pokemon(
                folium_map, pokemon_entity['lat'], pokemon_entity['lon'],
                pokemon['title_ru'], pokemon['img_url'])

    return render(request, "mainpage.html", context={'map': folium_map._repr_html_(),
                                                     'pokemons': pokemons})


def show_pokemon(request, pokedex_no):
    with open("pokemon_entities/pokemons.json") as database:
        pokemons = json.load(database)['pokemons']

    for pokemon in pokemons:
        if pokemon['pokedex_no'] == pokedex_no:
            requested_pokemon = pokemon
            break
    else:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in requested_pokemon['entities']:
        folium_map = add_pokemon(
            folium_map, pokemon_entity['lat'], pokemon_entity['lon'],
            pokemon['title_ru'], pokemon['img_url'])

    return render(request, "pokemon.html", context={'map': folium_map._repr_html_(),
                                                    'pokemon': pokemon})
