from django.shortcuts import render
from django.http import HttpResponse

import requests
import json

# data = [
#     {
#         'title': 'web Gymnazia Arabska',
#         'link': 'https://gyarab.cz',
#     },
#     {
#         'title': 'web jutub',
#         'link': 'https://youtube.com',
#     },
# ]

def homepage(request):
    with open('articles.json', encoding='utf-8') as f:
        articles = json.load(f)


    return render(request, 'content/homepage.html', {'articles': articles})

def article(request, id):
    with open('articles.json', encoding='utf-8') as f:
        articles = json.load(f)
    
    article = articles[id]

    return render(request, 'content/article.html', {'article' : article})

def hello(request, name):
    return HttpResponse(f'Ahoj {name}')

def vynasob(request, a, b):
    return HttpResponse(f'{a} * {b} = {a*b}')
