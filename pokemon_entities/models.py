from django.db import models
from django.utils.timezone import timezone


class Pokemon(models.Model):
    pokemon_id = models.IntegerField(1, null=True)
    title = models.CharField(max_length=200)
    title_en = models.CharField(max_length=200, blank=True)
    title_jp = models.CharField(max_length=200, blank=True)
    image = models.ImageField(blank=True)
    description = models.TextField(blank=True)
    # next_evolution = models.ForeignKey("self", on_delete=models.CASCADE, null=True)
    # previous_evolution = models.ForeignKey("self", on_delete=models.CASCADE, null=True)

    def previous_evolution(self):
        if self.pokemon_id == 0:
            return None
        else:
            pokemon = Pokemon.objects.get(pokemon_id=(self.pokemon_id-1))
            return pokemon

    def next_evolution(self):
        if self.pokemon_id > 2:
            return None
        else:
            pokemon = Pokemon.objects.get(pokemon_id=(self.pokemon_id+1))
            return pokemon


    def __str__(self):
        return f'{self.title}'


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    appeared_at = models.DateTimeField(null=True)
    disappeared_at = models.DateTimeField(null=True)
    level = models.IntegerField(default=0)
    health = models.IntegerField(default=0)
    strength = models.IntegerField(default=0)
    defence = models.IntegerField(default=0)
    stamina = models.IntegerField(default=0)


