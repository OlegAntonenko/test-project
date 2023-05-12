from django.contrib import admin
from places.models import Place
from django_admin_geomap import ModelAdmin


class Admin(ModelAdmin):
    geomap_field_longitude = "id_lon"
    geomap_field_latitude = "id_lat"


admin.site.register(Place, Admin)
