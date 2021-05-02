from rest_framework import serializers
from .models import Artist, Album, Track


class ArtistSerializer(serializers.ModelSerializer):

    class Meta:
        model=Artist
        # fields=('name')
        fields='__all__'

class AlbumSerializer(serializers.ModelSerializer):

    class Meta:
        model=Album
        # fields=('name')
        fields='__all__'

class TrackSerializer(serializers.ModelSerializer):

    class Meta:
        model=Track
        # fields=('name')
        fields='__all__'