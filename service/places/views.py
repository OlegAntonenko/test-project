import pandas as pd
from django.db import IntegrityError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from .serializers import UploadSerializer
from rest_framework import status
from .models import Places


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
                place, _ = Places.objects.update_or_create(
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
