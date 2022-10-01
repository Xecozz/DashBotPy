# basic
from django.http import HttpRequest
from django.shortcuts import redirect

# oaut2 discord
import requests
from django.contrib.auth import authenticate, login

# backend authentification
from django.contrib.auth.decorators import login_required

# admin
from django.utils import timezone
from django.contrib.sessions.models import Session

# Create your views here.

# redirect oauth2
redirect_url_discord = "https://discord.com/api/oauth2/authorize?client_id=1023285147681960069&redirect_uri=http%3A%2F%2F127.0.0.1%3A8000%2Foauth2%2Flogin%2Fredirect&response_type=code&scope=identify%20guilds"


@login_required(login_url="/oauth2/login")
def get_authenticated_user(request: HttpRequest) -> object:
    user = request.user
    return ({
        "id": user.id,
        "discord_tag": user.discord_tag,
        "avatar": user.avatar,
        "public_flags": user.public_flags,
        "flags": user.flags,
        "locale": user.locale,
        "mfa_enabled": user.mfa_enabled,
        "guilds": user.guilds,
    })


# redirect to discord url auth
def discord_login(request: HttpRequest):
    return redirect(redirect_url_discord)


# auth and login
def discord_login_redirect(request: HttpRequest):
    code = request.GET.get('code')
    user = exchange_code(code)
    discord_user = authenticate(request, user=user)
    discord_user = list(discord_user).pop()
    print(discord_user)
    login(request, discord_user, backend="discordAuth.auth.DiscordAuthentificationBackend")
    return redirect('/index/')


# change code with token
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
    print(credentials)
    access_token = credentials['access_token']

    responseUser = requests.get('https://discord.com/api/v10/users/@me', headers={
        'Authorization': 'Bearer %s' % access_token
    })
    responseGuild = requests.get('https://discord.com/api/v10/users/@me/guilds', headers={
        'Authorization': 'Bearer %s' % access_token
    })

    user = responseUser.json()

    print(responseUser)
    guilds_Json = responseGuild.json()

    guilds = []
    for guild in guilds_Json:
        if guild['owner']:
            guild_dico = {"id": guild['id'], "name": guild['name'], "icon": guild['icon'], "owner": guild['owner']}
            guilds.append(guild_dico)

    user['guilds'] = guilds

    return user


# Admin Session
def delete_all_unexpired_sessions_for_user(user):
    unexpired_sessions = Session.objects.filter(expire_date__gte=timezone.now())
    [
        session.delete() for session in unexpired_sessions
        if str(user.pk) == session.get_decoded().get('_auth_user_id')
    ]


def logout(request):
    delete_all_unexpired_sessions_for_user(request.user)
    return redirect("/admin/connexion")
