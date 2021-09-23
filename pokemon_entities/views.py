import folium

from django.http import HttpResponseNotFound
from django.shortcuts import render
from pokemon_entities.models import Pokemon, PokemonEntity


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
    pokemons = Pokemon.objects.all()

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon in pokemons:
        pokemon_entities = PokemonEntity.objects.filter(
            pokemon__title=pokemon.title
        )
        for pokemon_entity in pokemon_entities:
            add_pokemon(
                folium_map, pokemon_entity.lat,
                pokemon_entity.lon,
                request.build_absolute_uri(pokemon.photo.url)
            )

    pokemons_on_page = []
    for pokemon in pokemons:
        pokemon_description = {
            'pokemon_id': pokemon.id,
            'title_ru': pokemon.title,
        }
        if pokemon.photo:
            pokemon_description.update({'img_url': pokemon.photo.url})
        pokemons_on_page.append(pokemon_description)

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    try:
        pokemon = Pokemon.objects.get(id=int(pokemon_id))
    except Pokemon.DoesNotExist:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    pokemon_entities = PokemonEntity.objects.filter(
        pokemon__title=pokemon.title
    )
    for pokemon_entity in pokemon_entities:
        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon,
            request.build_absolute_uri(pokemon.photo.url)
        )

    pokemon_description = {
        'img_url': request.build_absolute_uri(pokemon.photo.url),
        'title_ru': pokemon.title,
        'title_en': pokemon.title_en,
        'title_jp': pokemon.title_jp,
        'description': pokemon.description,
    }

    if pokemon.previous_evolution:
        pokemon_ancestor = pokemon.previous_evolution
        pokemon_description.update(
            {
                'previous_evolution': {
                    'pokemon_id': pokemon_ancestor.id,
                    'img_url': pokemon_ancestor.photo.url,
                    'title_ru': pokemon_ancestor.title,
                }
            }
        )

    if pokemon.next_evolutions.all():
        pokemon_descendant = pokemon.next_evolutions.all()[0]
        pokemon_description.update(
            {
                'next_evolution': {
                    'pokemon_id': pokemon_descendant.id,
                    'img_url': pokemon_descendant.photo.url,
                    'title_ru': pokemon_descendant.title,
                }
            }
        )

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon_description
    })
