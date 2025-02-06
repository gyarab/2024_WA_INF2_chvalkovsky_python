from django.shortcuts import render
from django.http import HttpResponse

import requests

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
    ret = '''
    <!DOCTYPE html>
    <html>
    <head></head>
    <body>
    <ul>
    '''

    url = 'https://kf-ga.github.io/_downloads/55747ce1b3aa6fea6b8a71e2b55912de/articles.json'
    res = requests.get(url)
    res.raise_for_status()
    data = res.json()

    for i in data:
        ret += f"""
        <li>
            {i['category']} <a href="{i['link']}">
                {i['title']}
            </a><br>
            <img src="{i['image']}">
            <p>{i['perex']}</p>
        </li>"""

    ret += "</ul></body></html>"
    return HttpResponse(ret)