from django.db import models  # noqa F401


class Pokemon(models.Model):
    title = models.CharField('Название', max_length=200)
    title_en = models.CharField('Английское название', max_length=200, blank=True)
    title_jp = models.CharField('Японское название', max_length=200, blank=True)
    description = models.TextField('Описание', blank=True)
    image = models.ImageField('Картинка', null=True, blank=True)
    previous_evolution = models.ForeignKey(
        "Pokemon",
        on_delete=models.SET_NULL,
        verbose_name='Предыдущая эволюция',
        null=True,
        blank=True,
        related_name="next_evolutions",
    )

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    latitude = models.FloatField('Широта')
    longitude = models.FloatField('Долгота')
    appeared_at = models.DateTimeField('Время появления')
    disappeared_at = models.DateTimeField('Время исчезновения')
    level = models.IntegerField('Уровень', blank=True, default=0)
    health = models.IntegerField('Здоровье', blank=True, default=0)
    strength = models.IntegerField('Атака', blank=True, default=0)
    defence = models.IntegerField('Защита', blank=True, default=0)
    stamina = models.IntegerField('Выносливость', blank=True, default=0)

    def __str__(self):
        return f"{self.pokemon}: {self.latitude}, {self.longitude}"
