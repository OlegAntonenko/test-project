from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Places(models.Model):
    """
    Модель 'Примечательные места'
    """
    name = models.CharField(max_length=100)
    rate = models.IntegerField(default=1)
    latitude = models.FloatField()
    longitude = models.FloatField()

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(rate__gte=1) & models.Q(rate__lte=25),
                name="rate range",
            ),
            models.CheckConstraint(
                check=models.Q(longitude__gte=-180.0) & models.Q(longitude__lte=180.0),
                name='longitude range'
            ),
            models.CheckConstraint(
                check=models.Q(latitude__gte=-90.0) & models.Q(latitude__lte=90.0),
                name='latitude range'
            ),
        ]

