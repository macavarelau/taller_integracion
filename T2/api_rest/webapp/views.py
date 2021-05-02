from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Artist, Album, Track
from .serializers import ArtistSerializer, AlbumSerializer, TrackSerializer
from base64 import b64encode

# Create your views here.
route = "https://t2-taller-integracion-mvarela2.herokuapp.com/"

def encode(word):

    encoded = b64encode(word.encode()).decode('utf-8')
    return encoded[0:22]

def validate_uniqueness(modelo, identificador):

    if modelo == "artist":
        artists = Artist.objects.all()
        serializer = ArtistSerializer(artists, many=True)
        encontrado = False
        for i in range(len(serializer.data)):
            if identificador == serializer.data[i]["id"]:
                encontrado = True
        return encontrado
    elif modelo == "album":
        albums = Album.objects.all()
        serializer = AlbumSerializer(albums, many=True)
        encontrado = False
        for i in range(len(serializer.data)):
            if identificador == serializer.data[i]["id"]:
                encontrado = True
        return encontrado
    else:
        tracks = Track.objects.all()
        serializer = TrackSerializer(tracks, many=True)
        encontrado = False
        for i in range(len(serializer.data)):
            if identificador == serializer.data[i]["id"]:
                encontrado = True
        return encontrado


class ArtistList(APIView):

    def get(self, request):
        artists = Artist.objects.all()
        serializer = ArtistSerializer(artists, many=True)
        arreglo = []
        for i in range(len(serializer.data)):
            dicc = dict()
            dicc["id"] = serializer.data[i]["id"]
            dicc["name"] = serializer.data[i]["name"]
            dicc["age"] = serializer.data[i]["age"]
            dicc["albums"] = route + "/artists/" + dicc["id"] + "/albums"
            dicc["tracks"] = route + "artists/" + dicc["id"] + "/tracks"
            dicc["self"] = route + "artists/" + dicc["id"]
            arreglo.append(dicc)
        return Response({'mensaje': "Resultados obtenidos", 'body': arreglo}, status = status.HTTP_200_OK)

    
    def post(self, request):
        
        if "age" not in request.data or "name" not in request.data:
            return Response({'mensaje': "Input inválido"}, status=status.HTTP_400_BAD_REQUEST)
        artist = dict()
        artist["name"] = request.data["name"]
        artist["age"] = request.data["age"]
        artist["id"] = encode(artist["name"])

        if validate_uniqueness("artist", artist["id"]):
            return Response({'mensaje': "Artista ya existe"}, status = status.HTTP_409_CONFLICT)

        serializer = ArtistSerializer(data = artist)

        arreglo = []
        if serializer.is_valid():
            serializer.save()
            dicc = dict()
            dicc["id"] = serializer.data["id"]
            dicc["name"] = serializer.data["name"]
            dicc["age"] = serializer.data["age"]
            dicc["albums"] = route + "/artists/" + dicc["id"] + "/albums"
            dicc["tracks"] = route + "artists/" + dicc["id"] + "/tracks"
            dicc["self"] = route + "artists/" + dicc["id"]
            arreglo.append(dicc)
            return Response({'mensaje': "Artista creado", 'body': arreglo}, status = status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        

    def put(self, request, id):
        if not validate_uniqueness("artist", id):
            return Response({'mensaje': "Artista no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        albums = Album.objects.all().filter(artist_id = id)
        serializer_album = AlbumSerializer(albums, many=True)
        for i in range(len(serializer_album.data)):
            tracks = Track.objects.all().filter(album_id = serializer_album.data[i]["id"])
            serializer_track = TrackSerializer(tracks, many=True)
            for j in range(len(serializer_track.data)):
                actual = dict()
                actual["times_played"] = serializer_track.data[j]["times_played"] + 1
                track = Track.objects.get(id = serializer_track.data[j]["id"])
                serializer = TrackSerializer(track, data=actual, partial=True)
                if serializer.is_valid():
                    serializer.save()
        return Response({'mensaje': "Todas las canciones del artista fueron reproducidas"}, status = status.HTTP_200_OK)

class ArtistSimple(APIView):

    def get(self, request, id):
        if not validate_uniqueness("artist", id):
            return Response({'mensaje': "Artista no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        artist = Artist.objects.get(id = id)
        serializer = ArtistSerializer(artist)
        arreglo = []
        dicc = dict()
        dicc["id"] = serializer.data["id"]
        dicc["name"] = serializer.data["name"]
        dicc["age"] = serializer.data["age"]
        dicc["albums"] = route + "artists/" + dicc["id"] + "/albums"
        dicc["tracks"] = route + "artists/" + dicc["id"] + "/tracks"
        dicc["self"] = route + "artists/" + dicc["id"]
        arreglo.append(dicc)
        return Response({'mensaje': "Operación exitosa", 'body': arreglo}, status = status.HTTP_200_OK)

    def delete(self, request, id):
        
        if not validate_uniqueness("artist", id):
            return Response({'mensaje': "Artista inexistente"}, status=status.HTTP_404_NOT_FOUND)
        artist = Artist.objects.get(id = id)
        serializer = ArtistSerializer(artist)
        if validate_uniqueness("artist", serializer.data["id"]):
            artist.delete()
            return Response({'mensaje': "Artista eliminado"}, status = status.HTTP_204_NO_CONTENT)

class ArtistAlbums(APIView):

    def get(self, request, artist_id):
        if not validate_uniqueness("artist", artist_id):
            return Response({'mensaje': "Artista no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        albums = Album.objects.all().filter(artist_id = artist_id)
        serializer = AlbumSerializer(albums, many=True)
        arreglo = []
        for i in range(len(serializer.data)):
            dicc = dict()
            dicc["id"] = serializer.data[i]["id"]
            dicc["artist_id"] = serializer.data[i]["artist_id"]
            dicc["name"] = serializer.data[i]["name"]
            dicc["genre"] = serializer.data[i]["genre"]
            dicc["artist"] = route + "artists/" + dicc["artist_id"]
            dicc["tracks"] = route + "albums/" + dicc["id"] + "/tracks"
            dicc["self"] = route + "albums/" + dicc["id"]
            arreglo.append(dicc)
        return Response({'mensaje': "Resultados obtenidos", 'body': arreglo}, status = status.HTTP_200_OK)

    def post(self, request, artist_id):

        if "name" not in request.data or "genre" not in request.data:
            return Response({'mensaje': "Input inválido"}, status=status.HTTP_400_BAD_REQUEST)
        if not validate_uniqueness("artist", artist_id):
            return Response({'mensaje': "Artista no existe"}, status = status.HTTP_422_UNPROCESSABLE_ENTITY)
        album = dict()
        album["name"] = request.data["name"]
        album["genre"] = request.data["genre"]
        string = album["name"] + ":" + artist_id
        album["id"] = encode(string)

        if validate_uniqueness("album", album["id"]):
            return Response({'mensaje': "Álbum ya existe"}, status = status.HTTP_409_CONFLICT)

        artist = Artist.objects.get(id = artist_id)
        serializer_artist = ArtistSerializer(artist)
        album["artist_id"] = serializer_artist.data["id"]

        serializer = AlbumSerializer(data = album)

        arreglo = []
        if serializer.is_valid():
            serializer.save()
            dicc = dict()
            dicc["id"] = serializer.data["id"]
            dicc["artist_id"] = serializer.data["artist_id"]
            dicc["name"] = serializer.data["name"]
            dicc["genre"] = serializer.data["genre"]
            dicc["artist"] = route + "artists/" + dicc["artist_id"]
            dicc["tracks"] = route + "albums/" + dicc["id"] + "/tracks"
            dicc["self"] = route + "albums/" + dicc["id"]
            arreglo.append(dicc)
            return Response({'mensaje': "Álbum creado", 'body': arreglo}, status = status.HTTP_201_CREATED)

class ArtistTracks(APIView):
    
    def get(self, request, id):
        if not validate_uniqueness("artist", id):
            return Response({'mensaje': "Artista no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        albums = Album.objects.all().filter(artist_id = id)
        serializer_album = AlbumSerializer(albums, many=True)
        arreglo = []
        for i in range(len(serializer_album.data)):
            tracks = Track.objects.all().filter(album_id = serializer_album.data[i]["id"])
            serializer = TrackSerializer(tracks, many=True)
            for j in range(len(serializer.data)):
                dicc = dict()
                dicc["id"] = serializer.data[j]["id"]
                dicc["album_id"] = serializer.data[j]["album_id"]
                dicc["name"] = serializer.data[j]["name"]
                dicc["duration"] = serializer.data[j]["duration"]
                dicc["times_played"] = serializer.data[j]["times_played"]
                dicc["artist"] = route + "artists/" + serializer_album.data[i]["artist_id"]
                dicc["tracks"] = route + "albums/" + dicc["album_id"]
                dicc["self"] = route + "tracks/" + dicc["id"]
                arreglo.append(dicc)
        return Response({'mensaje': "Resultados obtenidos", 'body': arreglo}, status = status.HTTP_200_OK)

class AlbumList(APIView):

    def get(self, request):
        albums = Album.objects.all()
        serializer = AlbumSerializer(albums, many=True)
        arreglo = []
        for i in range(len(serializer.data)):
            dicc = dict()
            dicc["id"] = serializer.data[i]["id"]
            dicc["artist_id"] = serializer.data[i]["artist_id"]
            dicc["name"] = serializer.data[i]["name"]
            dicc["genre"] = serializer.data[i]["genre"]
            dicc["artist"] = route + "artists/" + dicc["artist_id"]
            dicc["tracks"] = route + "albums/" + dicc["id"] + "/tracks"
            dicc["self"] = route + "albums/" + dicc["id"]
            arreglo.append(dicc)
        return Response({'mensaje': "Resultados obtenidos", 'body': arreglo}, status = status.HTTP_200_OK)
    

    def put(self, request, id):

        if not validate_uniqueness("album", id):
            return Response({'mensaje': "Álbum no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        tracks = Track.objects.all().filter(album_id = id)
        serializer_track = TrackSerializer(tracks, many=True)
        for i in range(len(serializer_track.data)):
            actual = dict()
            actual["times_played"] = serializer_track.data[i]["times_played"] + 1
            track = Track.objects.get(id = serializer_track.data[i]["id"])
            serializer = TrackSerializer(track, data=actual, partial=True)
            if serializer.is_valid():
                serializer.save()
        return Response({'mensaje': "Canciones del álbum reproducidas"}, status = status.HTTP_200_OK)

class AlbumSimple(APIView):

    def get(self, request, id):
        if not validate_uniqueness("album", id):
            return Response({'mensaje': "Álbum no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        album = Album.objects.get(id = id)
        serializer = AlbumSerializer(album)
        arreglo = []
        dicc = dict()
        dicc["id"] = serializer.data["id"]
        dicc["artist_id"] = serializer.data["artist_id"]
        dicc["name"] = serializer.data["name"]
        dicc["genre"] = serializer.data["genre"]
        dicc["artist"] = route + "artists/" + dicc["artist_id"]
        dicc["tracks"] = route + "albums/" + dicc["id"] + "/tracks"
        dicc["self"] = route + "albums/" + dicc["id"]
        arreglo.append(dicc)
        return Response({'mensaje': "Operación exitosa", 'body': arreglo}, status = status.HTTP_200_OK)

    def delete(self, request, id):

        if not validate_uniqueness("album", id):
            return Response({'mensaje': "Álbum no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        album = Album.objects.get(id = id)
        serializer = AlbumSerializer(album)
        if validate_uniqueness("album", serializer.data["id"]):
            album.delete()
            return Response({'mensaje': "Álbum eliminado"}, status = status.HTTP_204_NO_CONTENT)

class AlbumsTracks(APIView):

    def get(self, request, id):
        if not validate_uniqueness("album", id):
            return Response({'mensaje': "Álbum no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        tracks = Track.objects.all().filter(album_id = id)
        serializer = TrackSerializer(tracks, many=True)
        arreglo = []
        for i in range(len(serializer.data)):
            dicc = dict()
            dicc["id"] = serializer.data[i]["id"]
            dicc["album_id"] = serializer.data[i]["album_id"]
            dicc["name"] = serializer.data[i]["name"]
            dicc["duration"] = serializer.data[i]["duration"]
            dicc["times_played"] = serializer.data[i]["times_played"]
            album = Album.objects.get(id = serializer.data[i]["album_id"])
            serializer_album = AlbumSerializer(album)
            dicc["artist"] = route + "artists/" + serializer_album.data["artist_id"]
            dicc["album"] = route + "albums/" + dicc["album_id"]
            dicc["self"] = route + "tracks/" + dicc["id"]
            arreglo.append(dicc)
        return Response({'mensaje': "Resultados obtenidos", 'body': arreglo}, status = status.HTTP_200_OK)

    def post(self, request, id):

        if "name" not in request.data or "duration" not in request.data:
            return Response({'mensaje': "Input inválido"}, status=status.HTTP_400_BAD_REQUEST)
        if not validate_uniqueness("album", id):
            return Response({'mensaje': "Álbum no existe"}, status = status.HTTP_422_UNPROCESSABLE_ENTITY)
        track = dict()
        track["name"] = request.data["name"]
        track["duration"] = request.data["duration"]
        track["times_played"] = 0
        string = track["name"] + ":" + id
        track["id"] = encode(string)

        if validate_uniqueness("track", track["id"]):
            return Response({'mensaje': "Canción ya existe"}, status = status.HTTP_409_CONFLICT)

        album = Album.objects.get(id = id)
        serializer_album = AlbumSerializer(album)
        track["album_id"] = serializer_album.data["id"]

        serializer = TrackSerializer(data = track)

        arreglo = []
        if serializer.is_valid():
            serializer.save()
            dicc = dict()
            dicc["id"] = serializer.data["id"]
            dicc["album_id"] = serializer.data["album_id"]
            dicc["name"] = serializer.data["name"]
            dicc["duration"] = serializer.data["duration"]
            dicc["times_played"] = serializer.data["times_played"]
            album = Album.objects.get(id = serializer.data["album_id"])
            serializer_album = AlbumSerializer(album)
            dicc["artist"] = route + "artists/" + serializer_album.data["artist_id"]
            dicc["tracks"] = route + "albums/" + dicc["album_id"]
            dicc["self"] = route + "tracks/" + dicc["id"]
            arreglo.append(dicc)
            return Response({'mensaje': "Canción creada", 'body': arreglo}, status = status.HTTP_201_CREATED)
             

class TrackList(APIView):

    def get(self, request):
        tracks=Track.objects.all()
        serializer=TrackSerializer(tracks, many=True)
        arreglo = []
        for i in range(len(serializer.data)):
            dicc = dict()
            dicc["id"] = serializer.data[i]["id"]
            dicc["album_id"] = serializer.data[i]["album_id"]
            dicc["name"] = serializer.data[i]["name"]
            dicc["duration"] = serializer.data[i]["duration"]
            dicc["times_played"] = serializer.data[i]["times_played"]
            album = Album.objects.get(id = serializer.data[i]["album_id"])
            serializer_album = AlbumSerializer(album)
            dicc["artist"] = route + "artists/" + serializer_album.data["artist_id"]
            dicc["album"] = route + "albums/" + dicc["album_id"]
            dicc["self"] = route + "tracks/" + dicc["id"]
            arreglo.append(dicc)
        return Response({'mensaje': "Operación exitosa", 'body': arreglo}, status = status.HTTP_200_OK)

    def put(self, request, id):

        if not validate_uniqueness("track", id):
            return Response({'mensaje': "Canción no encontrada"}, status=status.HTTP_404_NOT_FOUND)
        track = Track.objects.get(id = id)
        serializer = TrackSerializer(track)
        actual = dict()
        actual["times_played"] = serializer.data["times_played"] + 1
        serializer = TrackSerializer(track, data=actual, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensaje': "Canción reproducida"}, status = status.HTTP_200_OK)

class TrackSimple(APIView):

    def get(self, request, id):
        if not validate_uniqueness("track", id):
            return Response({'mensaje': "Canción no encontrada"}, status=status.HTTP_404_NOT_FOUND)
        track = Track.objects.get(id = id)
        serializer = TrackSerializer(track)
        arreglo = []
        dicc = dict()
        dicc["id"] = serializer.data["id"]
        dicc["album_id"] = serializer.data["album_id"]
        dicc["name"] = serializer.data["name"]
        dicc["duration"] = serializer.data["duration"]
        dicc["times_played"] = serializer.data["times_played"]
        album = Album.objects.get(id = serializer.data["album_id"])
        serializer_album = AlbumSerializer(album)
        dicc["artist"] = route + "artists/" + serializer_album.data["artist_id"]
        dicc["tracks"] = route + "albums/" + dicc["album_id"]
        dicc["self"] = route + "tracks/" + dicc["id"]
        arreglo.append(dicc)
        return Response({'mensaje': "Operación exitosa", 'body': arreglo}, status = status.HTTP_200_OK)

    def delete(self, request, id):
        
        if not validate_uniqueness("track", id):
            return Response({'mensaje': "Canción inexistente"}, status=status.HTTP_404_NOT_FOUND)
        track = Track.objects.get(id = id)
        serializer = TrackSerializer(track)
        if validate_uniqueness("track", serializer.data["id"]):
            track.delete()
            return Response({'mensaje': "Canción eliminada"}, status = status.HTTP_204_NO_CONTENT)