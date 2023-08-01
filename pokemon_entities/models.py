from django.db import models  # noqa F401
from django.utils.timezone import now

class Pokemon(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    title = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='images', null=True, blank=True)
    appeared_at = models.DateTimeField(default=now)
    disappeared_at = models.DateTimeField(default=now)
    def __str__(self):
        return '{}'.format(self.title)
    

class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    lat = models.FloatField()
    lon = models.FloatField()
    