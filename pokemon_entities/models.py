from django.db import models


class Pokemon(models.Model):
    pokemon_id = models.IntegerField(verbose_name='Номер_эволюции', default=1, unique=True)
    title = models.CharField(max_length=200, verbose_name='Имя')
    image = models.ImageField(verbose_name='Изображение')
    description = models.TextField(blank=True, verbose_name='Описание')
    title_en = models.CharField(max_length=200, blank=True, verbose_name='Английское_имя')
    title_jp = models.CharField(max_length=200, blank=True, verbose_name='Японское_имя')
    previous_evolution = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='next_evolutions',
        verbose_name='предыдущая эволюция',
        on_delete=models.SET_NULL
    )

    def __str__(self):
        return f'{self.title}'


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, verbose_name='Покемон', related_name='entity')
    appeared_at = models.DateTimeField(blank=True, null=True, verbose_name='Время_появления')
    disappeared_at = models.DateTimeField(blank=True, null=True, verbose_name='Время_исчезания')
    latitude = models.FloatField(blank=True, null=True, verbose_name='Широта')
    longitude = models.FloatField(blank=True, null=True, verbose_name='Долгота')
    level = models.IntegerField(blank=True, null=True, verbose_name='Уровень')
    health = models.IntegerField(blank=True, null=True, verbose_name='Здоровье')
    strength = models.IntegerField(blank=True, null=True, verbose_name='Сила')
    defence = models.IntegerField(blank=True, null=True, verbose_name='Защита')
    stamina = models.IntegerField(blank=True, null=True, verbose_name='Выносливость')

    def __str__(self):
        return f'{self.pokemon.title}'

