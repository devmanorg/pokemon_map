from django.db import models  # noqa F401

class Pokemon(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    title = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='images', null=True, blank=True)
    def __str__(self):
        return '{}'.format(self.title)
    

class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    lat = models.FloatField()
    lon = models.FloatField()
    