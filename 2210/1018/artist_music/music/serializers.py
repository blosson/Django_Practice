from dataclasses import field
from rest_framework import serializers
from .models import Artist, Music

class ArtistListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Artist
        fields = ('id', 'name',)


class MusicListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Music
        fields = ('id', 'title')
        read_only_fields = ('artist',)


class MusicSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Music
        fields = ('id', 'title', 'artist')  # 이거 좀 고민해봐야겠다.
        read_only_fields = ('artist',)      # 이것두


  
class ArtistSerializer(serializers.ModelSerializer):
    # music_set = serializers.PrimaryKeyRealatedField(many=True, read_only=True)
    music_set = MusicSerializer(many=True, read_only=True)
    music_count = serializers.IntegerField(source='music_set.count', read_only=True)
    
    class Meta:
        model = Artist
        fields = ('id', 'name', 'music_set', 'music_count')