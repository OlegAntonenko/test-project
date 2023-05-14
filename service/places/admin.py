from django.contrib import admin
from places.models import Place, Whether
from django_admin_geomap import ModelAdmin


class Admin(ModelAdmin):
    geomap_field_longitude = "id_lon"
    geomap_field_latitude = "id_lat"


class WhetherAdmin(admin.ModelAdmin):
    readonly_fields = ('atmosphere_pressure', 'air_humidity', 'direction_wind', 'wind_speed', 'place', 'temperature'
                       , 'date')


admin.site.register(Place, Admin)
admin.site.register(Whether, WhetherAdmin)
