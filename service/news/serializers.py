from rest_framework import serializers

from news.models import News


class NewsSerializers(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['title', 'image', 'text', 'author', 'date', 'preview']
        extra_kwargs = {
            'image': {'write_only': True},
            'preview': {'read_only': True},
        }
