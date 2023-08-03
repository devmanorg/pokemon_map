from django.db import models  # noqa F401
from django.utils.timezone import now

class Pokemon(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    title = models.CharField(max_length=200, blank=True)
    title_en = models.CharField(max_length=200, blank=True)
    title_jp = models.CharField(max_length=200, blank=True)
    photo = models.ImageField(upload_to='images', null=True, blank=True)
    appeared_at = models.DateTimeField(default=now)
    disappeared_at = models.DateTimeField(default=now)
    description = models.CharField(max_length=400, blank=True)
    level = models.IntegerField(blank=True)
    health = models.IntegerField(blank=True)
    strength = models.IntegerField(blank=True)
    defence = models.IntegerField(blank=True)
    stamina = models.IntegerField(blank=True)
    previous_evolution = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True, related_name='next_gen' )
    def __str__(self):
        return '{}'.format(self.title)
    

class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    lat = models.FloatField()
    lon = models.FloatField()
    