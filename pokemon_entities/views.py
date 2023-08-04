import folium
from django.utils.timezone import localtime, now
from django.http import HttpResponseNotFound
from django.shortcuts import render
from .models import Pokemon, PokemonEntity
from pytz import timezone


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    pokemons = Pokemon.objects.filter(disappeared_at__gt=localtime(now()), appeared_at__lt=localtime(now()))
    for pokemon in pokemons:
        for pokemon_entity in PokemonEntity.objects.all():
            if pokemon == pokemon_entity.pokemon:
                add_pokemon(
                    folium_map, pokemon_entity.lat,
                    pokemon_entity.lon,
                    request.build_absolute_uri(f'/media/{pokemon_entity.pokemon.photo}')
                )

    pokemons_on_page = []
    for pokemon in Pokemon.objects.all():
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': request.build_absolute_uri(f'/media/{pokemon.photo}'),
            'title_ru': pokemon.title,
        })
    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    try:
        pokemon = Pokemon.objects.get(id = int(pokemon_id))
        previous_evolution, next_evolution = {}, {}
        if pokemon.previous_evolution:
            previous_evolution = {"title_ru": pokemon.previous_evolution.title,
                            "pokemon_id": pokemon.previous_evolution.id,
                            "img_url": request.build_absolute_uri(f'/media/{pokemon.previous_evolution.photo}'),
                            }
        if pokemon.next_gen.first():
            next_evolution = {"title_ru": pokemon.next_gen.first().title,
                            "pokemon_id": pokemon.next_gen.first().id,
                            "img_url": request.build_absolute_uri(f'/media/{pokemon.next_gen.first().photo}'),
                            }
  
        requested_pokemon = {"pokemon_id":pokemon.id,
                         "title_ru":pokemon.title,
                         "title_en":pokemon.title_en,
                         "title_jp":pokemon.title_jp,
                         "img_url":request.build_absolute_uri(f'/media/{pokemon.photo}'),
                         "description":pokemon.description,
                         "previous_evolution": previous_evolution,
                         "next_evolution": next_evolution
                         }
    except:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    for pokemon_entity in PokemonEntity.objects.filter(pokemon=pokemon):
        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon,
            request.build_absolute_uri(f'/media/{pokemon_entity.pokemon.photo}')
        )

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': requested_pokemon
    })
