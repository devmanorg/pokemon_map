from django.db import models  # noqa F401


class Pokemon(models.Model):
    title = models.CharField('Название', max_length=200)
    image = models.ImageField('Картинка', null=True, blank=True)

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    latitude = models.FloatField('Широта')
    longitude = models.FloatField('Долгота')
    appeared_at = models.DateTimeField('Время появления')
    disappeared_at = models.DateTimeField('Время исчезновения')
    level = models.IntegerField('Уровень')
    health = models.IntegerField('Здоровье')
    strength = models.IntegerField('Атака')
    defence = models.IntegerField('Защита')
    stamina = models.IntegerField('Выносливость')
