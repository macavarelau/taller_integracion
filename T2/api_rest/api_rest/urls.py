"""api_rest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from webapp import views


urlpatterns = [
    path('admin', admin.site.urls),
    path('artists', views.ArtistList.as_view()), #funciona
    path('artists/<id>', views.ArtistSimple.as_view()), #funciona
    path('artists/<artist_id>/albums', views.ArtistAlbums.as_view()), #funciona
    path('artists/<id>/tracks', views.ArtistTracks.as_view()), #funciona
    path('artists/<id>/albums/play', views.ArtistList.as_view()), #funciona
    path('albums', views.AlbumList.as_view()), #funciona
    path('albums/<id>', views.AlbumSimple.as_view()), #funciona
    path('albums/<id>/tracks', views.AlbumsTracks.as_view()), #funciona
    path('albums/<id>/tracks/play', views.AlbumList.as_view()), #funciona
    path('tracks', views.TrackList.as_view()), #funciona
    path('tracks/<id>', views.TrackSimple.as_view()), #funciona
    path('tracks/<id>/play', views.TrackList.as_view()) #funciona
]
