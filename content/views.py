from django.shortcuts import render, get_object_or_404
from .models import Guitar
import json

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
    return render(request, 'content/homepage.html', {'guitars': guitars, 'page': 'homepage'})

def details(request, id):
    guitar = get_object_or_404(Guitar, id=id)
    return render(request, 'content/details.html', {'guitar': guitar, 'page': 'details'})