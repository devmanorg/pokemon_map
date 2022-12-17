from django.db import models  # noqa F401


class Pokemon(models.Model):
    title = models.CharField('Название', max_length=200)
    image = models.ImageField('Картинка', null=True, blank=True)

    def __str__(self):
        return self.title
    

class PokemonEntity(models.Model):
    latitude = models.FloatField('Широта')
    longitude = models.FloatField('Долгота')
    