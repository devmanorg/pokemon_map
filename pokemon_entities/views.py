import json

from django.http import HttpResponseNotFound
from django.shortcuts import render


MOSCOW_CENTER = [55.751244, 37.618423]


def show_all_pokemons(request):
    with open('pokemon_entities/pokemons.json', encoding='utf-8') as database:
        pokemons = json.load(database)['pokemons']

    pokemon_markers = []
    for pokemon in pokemons:
        for pokemon_entity in pokemon['entities']:
            pokemon_markers.append({
                "lat": pokemon_entity['lat'],
                "lon": pokemon_entity['lon'],
                "image_url": pokemon['img_url'],
            })

    pokemons_on_page = []
    for pokemon in pokemons:
        pokemons_on_page.append({
            'pokemon_id': pokemon['pokemon_id'],
            'img_url': pokemon['img_url'],
            'title_ru': pokemon['title_ru'],
        })

    return render(request, 'mainpage.html', context={
        'pokemons': pokemons_on_page,
        'pokemon_markers': pokemon_markers,
        'moscow_center': MOSCOW_CENTER,
    })


def show_pokemon(request, pokemon_id):
    with open('pokemon_entities/pokemons.json', encoding='utf-8') as database:
        pokemons = json.load(database)['pokemons']

    for pokemon in pokemons:
        if pokemon['pokemon_id'] == int(pokemon_id):
            requested_pokemon = pokemon
            break
    else:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    return render(request, 'pokemon.html', context={
        'pokemon': requested_pokemon,
        'moscow_center': MOSCOW_CENTER,
    })