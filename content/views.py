from django.shortcuts import render
from django.http import HttpResponse

import requests
import json

def homepage(request):
    with open('guitars.json', encoding='utf-8') as f:
        guitars = json.load(f)


    return render(request, 'content/homepage.html', {'guitars': guitars})

def details(request, id):
    with open('guitars.json', encoding='utf-8') as f:
        guitars = json.load(f)
    
    guitar = guitars[id]

    return render(request, 'content/details.html', {'guitar' : guitar})
