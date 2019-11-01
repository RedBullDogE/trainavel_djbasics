from django.db import models
from django.core.exceptions import ValidationError
from cities.models import City


class Train(models.Model):
    name = models.CharField(max_length=100, unique=True,
                            verbose_name='Номер поезда')
    from_city = models.ForeignKey(
        City, on_delete=models.CASCADE, verbose_name='Откуда', related_name='from_city')
    to_city = models.ForeignKey(
        City, on_delete=models.CASCADE, verbose_name='Куда', related_name='to_city')
    travel_time = models.IntegerField(verbose_name='Время в пути')

    class Meta:
        verbose_name = 'Поезд'
        verbose_name_plural = 'Поезда'
        ordering = ['name']

    def __str__(self):
        return f"Поезд №{self.name} из {self.from_city} в {self.to_city}"

    def clean(self, *args, **kwargs):
        if self.from_city == self.to_city:
            raise ValidationError('Некорректный город прибытия!')
        
        if self.travel_time <= 0:
            raise ValidationError('Некорректно задано время!')

        query = Train.objects.filter(from_city=self.from_city,  # pylint: disable=maybe-no-member
                                     to_city=self.to_city,
                                     travel_time=self.travel_time).exclude(pk=self.pk)

        if query.exists():
            raise ValidationError('Уже существует поезд на данном маршруте с таким же временем!')
        
        return super(Train, self).clean(*args, **kwargs)
