from django.shortcuts import render, redirect

from MusicApp.common.session_decorator import session_decorator
from MusicApp.musics.forms import AlbumCreateForm, AlbumUpdateForm, AlbumDeleteForm, SongCreateForm
from MusicApp.musics.models import Album
from MusicApp.settings import session


# Create your views here.
@session_decorator(session)
def index(request):
    albums = session.query(Album).all()

    context = {
        'albums': albums,
    }
    return render(request, 'common/index.html', context)


def create_album(request):
    if request.method == 'POST':
        form = AlbumCreateForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = AlbumCreateForm()

    context = {
        'form': form,
    }

    return render(request, 'albums/create-album.html', context)


@session_decorator(session)
def details_album(request, id: int):
    album = session.query(Album).filter_by(id=id).first()

    context = {
        'album': album,
    }
    return render(request, 'albums/album-details.html', context)


def edit_album(request, id: int):
    album = session.query(Album).filter_by(id=id).first()
    if request.method == 'POST':
        form = AlbumUpdateForm(request.POST)

        if form.is_valid():
            form.save(album)
            return redirect('index')

    else:
        initial = {
            "album_name": album.album_name,
            "image_url": album.image_url,
            "price": album.price,
        }

        form = AlbumUpdateForm(initial)

    context = {
        'album': album,
        'form': form,
    }

    return render(request, 'albums/edit-album.html', context)


def delete_album(request, id: int):
    album = session.query(Album).filter_by(id=id).first()

    if request.method == 'POST':
        session.delete(album)
        return redirect('index')
    else:
        initial = {
            "album_name": album.album_name,
            "image_url": album.image_url,
            "price": album.price,
        }
        form = AlbumDeleteForm(initial)

    context = {
        'album': album,
        'form': form,
    }

    return render(request, 'albums/delete-album.html', context)


def create_song(request):
    if request.method == 'POST':
        form = SongCreateForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('index')

    else:
        form = SongCreateForm(request.POST)

    context = {
        'form': form,
    }
    return render(request, 'songs/create-song.html', context)
