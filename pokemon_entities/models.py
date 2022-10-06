from django.db import models
from django.utils.timezone import timezone


class Pokemon(models.Model):
    pokemon_id = models.IntegerField(1, null=True)
    title = models.CharField(max_length=200, verbose_name='Имя')
    title_en = models.CharField(max_length=200, blank=True, verbose_name='Английское_имя')
    title_jp = models.CharField(max_length=200, blank=True, verbose_name='Японское_имя')
    image = models.ImageField(blank=True, verbose_name='Изображение')
    description = models.TextField(blank=True, verbose_name='Описание')

    def previous_evolution(self):
        if self.pokemon_id:
            pokemon = Pokemon.objects.get(pokemon_id=(self.pokemon_id - 1))
            return pokemon
        return None

    def next_evolution(self):
        count_pokemon_id = Pokemon.objects.values("pokemon_id").distinct().count()
        if self.pokemon_id >= count_pokemon_id:
            return None
        return Pokemon.objects.get(pokemon_id=(self.pokemon_id+1))

    def __str__(self):
        return f'{self.title}'


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, verbose_name='Покемон')
    latitude = models.FloatField(null=True, verbose_name='Широта')
    longitude = models.FloatField(null=True, verbose_name='Долгота')
    appeared_at = models.DateTimeField(null=True, verbose_name='Время_появления')
    disappeared_at = models.DateTimeField(null=True, verbose_name='Время_исчезания')
    level = models.IntegerField(default=0, verbose_name='Уровень')
    health = models.IntegerField(default=0, verbose_name='Здоровье')
    strength = models.IntegerField(default=0, verbose_name='Сила')
    defence = models.IntegerField(default=0, verbose_name='Защита')
    stamina = models.IntegerField(default=0, verbose_name='Выносливость')


