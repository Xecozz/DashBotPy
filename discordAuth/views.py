from django.http import JsonResponse, HttpResponse, HttpRequest
from django.shortcuts import render, redirect
import requests
from django.contrib.auth import authenticate, login
import json

# Create your views here.

redirect_url_discord = "https://discord.com/api/oauth2/authorize?client_id=1023285147681960069&redirect_uri=http%3A%2F%2F127.0.0.1%3A8000%2Foauth2%2Flogin%2Fredirect&response_type=code&scope=identify%20guilds"


def home(request: HttpRequest) -> JsonResponse:
    return JsonResponse({"msg": "hello"})


def discord_login(request: HttpRequest):
    return redirect(redirect_url_discord)


def discord_login_redirect(request: HttpRequest):
    code = request.GET.get('code')
    user, guilds= exchange_code(code)
    authenticate(request, user=user, guilds=guilds)
    return JsonResponse({"user": user, "guilds": guilds})


def exchange_code(code):
    data = {
        "client_id": "1023285147681960069",
        "client_secret": "Sfkq7KeSw-wgNMVidIfETgsFRYB6TK4N",
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": "http://127.0.0.1:8000/oauth2/login/redirect",
        "scope": "identify guild"
    }
    headers = {
        'Content_Type': 'application/x-www-form-urlencoded'
    }
    response = requests.post("https://discord.com/api/oauth2/token", data=data, headers=headers)

    credentials = response.json()
    access_token = credentials['access_token']

    responseUser = requests.get('https://discord.com/api/v10/users/@me', headers={
        'Authorization': 'Bearer %s' % access_token
    })
    responseGuild = requests.get('https://discord.com/api/v10/users/@me/guilds?id', headers={
        'Authorization': 'Bearer %s' % access_token
    })
    user = responseUser.json()
    guilds_Json = responseGuild.json()
    data = []
    for guild in guilds_Json:
        guild_dico = {"id" : guild['id'], "name" : guild['name'], "icon" : guild['icon'], "owner" : guild['owner']}
        data.append(guild_dico)
    guilds = json.dumps(data)
    print(user, guilds)
    return user, guilds
