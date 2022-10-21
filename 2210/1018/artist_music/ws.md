## serializers.py

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




## views.py

from django.shortcuts import render, get_object_or_404, get_list_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Artist, Music
from .serializers import ArtistListSerializer, ArtistSerializer, MusicListSerializer, MusicSerializer
from music import serializers



@api_view(['GET', 'POST'])
def artists_list(request):

    if request.method == 'GET':
        artists = get_list_or_404(Artist)
        serializer = ArtistListSerializer(artists, many=True)

        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ArtistSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        
            return Response(serializer.data, status=status.HTTP_201_CREATED)



@api_view(['GET'])
def artist_detail(request, artist_pk):
    artist = get_object_or_404(Artist, pk=artist_pk)

    if request.method == 'GET':
        serializer = ArtistSerializer(artist)

        return Response(serializer.data)


@api_view(['POST'])
def music_create(request, artist_pk):
    artist = get_object_or_404(Artist)
    serializer = MusicSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(artist=artist)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def musics_list(request):
    musics = get_list_or_404(Music)
    serializer = MusicListSerializer(musics, many=True)
    
    return Response(serializer.data)


@api_view(['GET', 'PUT', 'DELETE'])
def music_detail(request, music_pk):
    music = get_object_or_404(Music, pk=music_pk)

    if request.method == 'GET':
        serializer = MusicSerializer(music)

        return Response(serializer.data)

    elif request.method == 'DELETE':
        music.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)

    elif request.method == 'PUT':
        serializer = MusicSerializer(music, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response(serializer.data)


    