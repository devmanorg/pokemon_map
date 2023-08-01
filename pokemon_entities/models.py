from django.db import models  # noqa F401

class Pokemon(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    title = models.CharField(max_length=200)
    def __str__(self):
        return '{}'.format(self.title)
    

class PokemonEntity(models.Model):
    lat = models.FloatField()
    lon = models.FloatField()
    