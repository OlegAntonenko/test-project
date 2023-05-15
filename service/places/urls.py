from django.urls import path

from .views import WeatherReportView

urlpatterns = [
    path('report', WeatherReportView.as_view(), name='report'),
]
