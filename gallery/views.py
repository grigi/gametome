from django.shortcuts import render
from galeria.models import Album, Picture
from pure_pagination import Paginator, EmptyPage
from django.conf import settings

RESULTS_PER_PAGE = getattr(settings, 'RESULTS_PER_PAGE', 20)

# Create your views here.

def album_list(request):
    album_list = Album.objects.public_root_nodes()
    paginator = Paginator(album_list, RESULTS_PER_PAGE)
    try:
        page = int(request.GET.get('page', 1))
    except ValueError:
        page = 1
    try:
        album_list = paginator.page(page)
    except EmptyPage:
        album_list = paginator.page(paginator.num_pages)
            
    return render(request, 'gallery/album_list.html', {
        'object_list': album_list,
    })
    
def album_detail(request, slug):
    try:
        page = int(request.GET.get('page', 1))
    except ValueError:
        page = 1

    album = Album.objects.public().get(slug=slug)
    album_list = album.children.all()
    paginator = Paginator(album_list, RESULTS_PER_PAGE)
    try:
        album_list = paginator.page(page)
    except EmptyPage:
        album_list = paginator.page(paginator.num_pages)
        
    picture_list = album.ordered_pictures.all()
    paginator = Paginator(picture_list, RESULTS_PER_PAGE)
    try:
        picture_list = paginator.page(page)
    except EmptyPage:
        picture_list = paginator.page(paginator.num_pages)

    return render(request, 'gallery/album_detail.html', {
        'object': album,
        'album_list': album_list,
        'picture_list': picture_list,
    })
    
def picture_detail(request, album_slug, pk, slug):
    return render(request, 'gallery/picture_detail.html', {
        'object': Picture.objects.public().get(album__slug=album_slug, pk=pk, slug=slug),
    })
