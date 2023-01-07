from django.db import models  # noqa F401


class Pokemon(models.Model):
    title = models.CharField('Название (рус.)', max_length=200)
    title_en = models.CharField('Название (англ.)', max_length=200, blank=True)
    title_jp = models.CharField('Название (яп.)', max_length=200, blank=True)
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

    class Meta:
        verbose_name = 'Тип покемона'
        verbose_name_plural = 'Типы покемонов'


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(
        Pokemon,
        on_delete=models.CASCADE,
        verbose_name='Тип покемона',
        related_name='entities',
    )
    latitude = models.FloatField('Широта')
    longitude = models.FloatField('Долгота')
    appeared_at = models.DateTimeField('Время появления')
    disappeared_at = models.DateTimeField('Время исчезновения')
    level = models.IntegerField('Уровень', blank=True, null=True)
    health = models.IntegerField('Здоровье', blank=True, null=True)
    strength = models.IntegerField('Атака', blank=True, null=True)
    defence = models.IntegerField('Защита', blank=True, null=True)
    stamina = models.IntegerField('Выносливость', blank=True, null=True)

    def __str__(self):
        return f"{self.pokemon}: {self.latitude}, {self.longitude}"

    class Meta:
        verbose_name = 'Покемон'
        verbose_name_plural = 'Покемоны'
