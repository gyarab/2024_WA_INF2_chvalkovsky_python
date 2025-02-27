from django.shortcuts import render, get_object_or_404
from .models import Guitar
# import json

"""
# JSON Code
def homepage(request):
    with open('guitars.json', encoding='utf-8') as f:
        guitars = json.load(f)


    return render(request, 'content/homepage.html', {'guitars': guitars, 'page': 'homepage'})

def details(request, id):
    with open('guitars.json', encoding='utf-8') as f:
        guitars = json.load(f)
    
    guitar = guitars[id]

    return render(request, 'content/details.html', {'guitar' : guitar, 'page': 'details'})
"""

# Database Code
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
    guitar = get_object_or_404(Guitar, id=id)
    return render(request, 'content/details.html', {'guitar': guitar, 'page': 'details'})