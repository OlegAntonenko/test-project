import io
import pandas as pd
from xlsxwriter.workbook import Workbook
from django.db import IntegrityError
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from .serializers import UploadSerializer
from rest_framework import status
from .models import Place, Whether


class UploadViewSet(ViewSet):
    serializer_class = UploadSerializer

    def create(self, request):
        file_uploaded = request.FILES.get('file_uploaded')

        if not file_uploaded:
            return Response(
                data='Add file',
                status=status.HTTP_400_BAD_REQUEST
            )

        file_name = file_uploaded.name
        if not file_name.endswith('.xlsx'):
            return Response(
                data='File\'s extension must be *.xlsx',
                status=status.HTTP_400_BAD_REQUEST
            )

        df = pd.read_excel(file_uploaded)
        set_cols_df = set(list(df))
        set_cols = {'name', 'rate', 'latitude', 'longitude'}
        if set_cols != set_cols_df:
            return Response(
                data='Column\'s file does not match',
                status=status.HTTP_400_BAD_REQUEST
            )
        df = df.astype({'rate': int, 'latitude': float, 'longitude': float})

        for ind, row in df.iterrows():
            try:
                place, _ = Place.objects.update_or_create(
                    name=row['name'],
                    latitude=row['latitude'],
                    longitude=row['longitude'],
                    defaults={
                        'name': row['name'],
                        'rate': row['rate'],
                        'latitude': row['latitude'],
                        'longitude': row['longitude'],
                    },
                )
                place.save()
            except IntegrityError:
                return Response(
                    data="row {} is out of bounds".format(ind),
                    status=status.HTTP_400_BAD_REQUEST
                )

        return Response(data='Success')


class WeatherReportView(APIView):

    def get(self, request):
        weather = Whether.objects.all()

        if not weather:
            return Response(
                data='No data',
                status=status.HTTP_400_BAD_REQUEST
            )

        output = io.BytesIO()

        workbook = Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet()

        worksheet.autofilter('F1:G1')

        worksheet.write(0, 0, 'atmosphere pressure')
        worksheet.write(0, 1, 'air humidity')
        worksheet.write(0, 2, 'direction wind')
        worksheet.write(0, 3, 'wind speed')
        worksheet.write(0, 4, 'temperature')
        worksheet.write(0, 5, 'place')
        worksheet.write(0, 6, 'date')

        for num, w in enumerate(weather, 1):
            worksheet.write(num, 0, w.atmosphere_pressure)
            worksheet.write(num, 1, w.air_humidity)
            worksheet.write(num, 2, w.direction_wind)
            worksheet.write(num, 3, w.wind_speed)
            worksheet.write(num, 4, w.temperature)
            worksheet.write(num, 5, w.place.name)
            worksheet.write(num, 6, w.date.replace(tzinfo=None))

        formatdict = {'num_format': 'mm/dd/yyyy'}
        fmt = workbook.add_format(formatdict)

        worksheet.set_column('G:G', None, fmt)

        workbook.close()
        output.seek(0)
        response = HttpResponse(output.read(),
                                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response['Content-Disposition'] = "attachment; filename=report.xlsx"
        output.close()

        return response
