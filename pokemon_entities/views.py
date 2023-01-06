import folium

from django.utils import timezone
from django.http import HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from .models import Pokemon, PokemonEntity
from django.core.exceptions import ObjectDoesNotExist


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
    time_now = timezone.now()
    pokemon_entities = PokemonEntity.objects.filter(
        appeared_at__lte=time_now,
        disappeared_at__gte=time_now
    )
    for pokemon_entity in pokemon_entities:
        add_pokemon(
            folium_map,
            pokemon_entity.latitude,
            pokemon_entity.longitude,
            request.build_absolute_uri(pokemon_entity.pokemon.image.url)
        )

    pokemons_for_page = Pokemon.objects.all()
    pokemons_on_page = []
    for pokemon in pokemons_for_page:
        try:
            image_url = request.build_absolute_uri(
                pokemon.image.url
            )
        except:
            image = None
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': image_url,
            'title_ru': pokemon.title,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    try:
        pokemon = get_object_or_404(Pokemon, id=pokemon_id)
    except ObjectDoesNotExist:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    image_url = request.build_absolute_uri(pokemon.image.url)
    time_now = timezone.now()
    pokemon_entities = PokemonEntity.objects.filter(
        pokemon=pokemon,
        appeared_at__lte=time_now,
        disappeared_at__gte=time_now,
    )
    for pokemon_entity in pokemon_entities:
        add_pokemon(
            folium_map, 
            pokemon_entity.latitude,
            pokemon_entity.longitude,
            image_url
        )
    previous_evolution = {}
    if pokemon.previous_evolution:
        previous_evolution = {
            "title_ru": pokemon.previous_evolution.title,
            "pokemon_id": pokemon.previous_evolution.id,
            "img_url": request.build_absolute_uri(pokemon.previous_evolution.image.url),
            'description': pokemon.previous_evolution.description,
            'title_en': pokemon.previous_evolution.title_en,
            'title_jp': pokemon.previous_evolution.title_jp,
        }
    try:
        next_pokemon = pokemon.next_evolution.get()
        next_evolution = {
            "title_ru": next_pokemon.title,
            "pokemon_id": next_pokemon.id,
            "img_url": request.build_absolute_uri(next_pokemon.image.url)
        }
    except Pokemon.DoesNotExist:
        next_evolution = {}

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 
        'pokemon': {
            'pokemon_id': pokemon.id,
            'img_url': image_url,
            'title_ru': pokemon.title,
            'title_en': pokemon.title_en,
            'title_jp': pokemon.title_jp,
            'description': pokemon.description,
            'previous_evolution': previous_evolution,
            'next_evolution': next_evolution,
        }
    })
