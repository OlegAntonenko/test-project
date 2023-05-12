from django_admin_geomap import GeoItem
from django.db import models


class Place(models.Model, GeoItem):
    """
    Модель 'Примечательные места'
    """
    name = models.CharField(max_length=100)
    rate = models.IntegerField(default=1)
    lat = models.FloatField(null=True, blank=True)
    lon = models.FloatField(null=True, blank=True)

    @property
    def geomap_popup_view(self):
        return "<strong>{}</strong>".format(str(self))

    @property
    def geomap_popup_edit(self):
        return self.geomap_popup_view

    @property
    def geomap_popup_common(self):
        return self.geomap_popup_view

    @property
    def geomap_longitude(self):
        return '' if self.lon is None else str(self.lon)

    @property
    def geomap_latitude(self):
        return '' if self.lat is None else str(self.lat)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(rate__gte=1) & models.Q(rate__lte=25),
                name="rate range",
            ),
            models.CheckConstraint(
                check=models.Q(lon__gte=-180.0) & models.Q(lon__lte=180.0),
                name='longitude range'
            ),
            models.CheckConstraint(
                check=models.Q(lat__gte=-90.0) & models.Q(lat__lte=90.0),
                name='latitude range'
            ),
        ]

