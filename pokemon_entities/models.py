from django.db import models  # noqa F401
from django.utils.timezone import now

class Pokemon(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, verbose_name='Айди')
    title = models.CharField(max_length=200, verbose_name='Имя', blank=True)
    title_en = models.CharField(max_length=200, verbose_name='Имя по-английски', blank=True)
    title_jp = models.CharField(max_length=200, verbose_name='Имя по-японски', blank=True)
    photo = models.ImageField(upload_to='images', null=True, blank=True, verbose_name='Картинка')
    appeared_at = models.DateTimeField(default=now, verbose_name='Появится')
    disappeared_at = models.DateTimeField(default=now, verbose_name='Исчезнет')
    description = models.CharField(max_length=400, blank=True, verbose_name='Описание')
    level = models.IntegerField(blank=True, verbose_name='Уровень', null=True)
    health = models.IntegerField(blank=True, verbose_name='Здоровье', null=True)
    strength = models.IntegerField(blank=True, verbose_name='Атака', null=True)
    defence = models.IntegerField(blank=True, verbose_name='Защита', null=True)
    stamina = models.IntegerField(blank=True, verbose_name='Выносливость', null=True)
    previous_evolution = models.ForeignKey("self", verbose_name='Из кого эволюционирует', on_delete=models.SET_NULL, null=True, blank=True, related_name='next_gen' )
    def __str__(self):
        return '{}'.format(self.title)
    

class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, verbose_name='Покемон')
    lat = models.FloatField(verbose_name='Широта')
    lon = models.FloatField(verbose_name='Долгота')
    