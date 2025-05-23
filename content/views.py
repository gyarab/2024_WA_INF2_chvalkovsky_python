from django.shortcuts import render, get_object_or_404
from .models import Guitar, Genre, Brand

def homepage(request):
    guitars = Guitar.objects.all()
    brands = Guitar.objects.values_list('brand', flat=True).distinct()
    pickups = Guitar.objects.values_list('pickups', flat=True).distinct()
    shapes = Guitar.objects.values_list('shape', flat=True).distinct()

    return render(request, 'content/homepage.html', 
        {
        'page': 'homepage', 
        'guitars': guitars, 
        'brands': brands,
        'pickups' : pickups,
        'shapes' : shapes,
         })

def details(request, id):
    #guitar = get_object_or_404(Guitar, id=id)
    #genres = guitar.genre.all()

    guitar = Guitar.objects.prefetch_related('genre').get(pk=id)
    genre_ids = list(guitar.genre.values_list('id', flat=True))
    
    #print("Guitar:", guitar)
    #print(guitar.genre.all())
    return render(request, 'content/details.html',
        {
            'page': 'details',
            'guitar': guitar,
            'genre_ids': genre_ids,
        })

def genre(request, id):
    genre = get_object_or_404(Genre, pk=id)  # Ensures 404 if genre doesn't exist
    guitars = Guitar.objects.filter(genre=genre)  # Proper filtering

    return render(request, 'content/genre.html', {
        'page': 'genre',
        'genre': genre,
        'guitars': guitars,
    })

def brand(request, id):
    brand = Brand.objects.get(pk=id)
    return render(request, 'content/brand.html',
        {
            'page': 'brand',
            'brand': brand,
        })