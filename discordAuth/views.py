import asyncio

from discord.ext import ipc
# basic
from django.http import HttpRequest, Http404, HttpResponse
from django.shortcuts import redirect, get_object_or_404

# oaut2 discord
import requests
from django.contrib.auth import authenticate, login

# backend authentification
from django.contrib.auth.decorators import login_required

# admin
from django.utils import timezone
from django.contrib.sessions.models import Session

from discordAuth.models import RefreshToken, DiscordUser

from packages.log import  LogInit

# logger
logger = LogInit("discordAuth.views").logger


ipc_client = ipc.Client(secret_key="pynel")

# redirect oauth2
redirect_url_discord = "https://discord.com/api/oauth2/authorize?client_id=1023285147681960069&redirect_uri=http%3A" \
                       "%2F%2F127.0.0.1%3A8000%2Foauth2%2Flogin%2Fredirect&response_type=code&scope=identify%20guilds "


# authentificate user
@login_required(login_url="/oauth2/login")
def get_authenticated_user(request: HttpRequest):
    user = request.user

    return ({
        "id": user.id,
        "discord_tag": user.discord_tag,
        "username": user.username,
        "tag": user.tag,
        "premium_type": user.premium_type,
        "avatar": user.avatar,
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
    user, refresh_token = ExchangeDiscord.exchange_code(code)

    if not user:
        return HttpResponse('Error with DiscordAuth retry or contact')

    # check bdd if refresh token
    find_token_len = RefreshToken.objects.filter(id=user['id'])
    if len(find_token_len) == 0:
        # create refreshToken
        RefreshToken.objects.create_token_refresh(user, refresh_token)
    else:
        # check is equal
        DiscordVerification.check_refresh_token(user, refresh_token)

    # autenticate
    discord_user = authenticate(request, user=user)
    discord_user = list(discord_user).pop()

    # login
    login(request, discord_user, backend="discordAuth.auth.DiscordAuthentificationBackend")

    logger.info(f"{user['username']} ({user['id']}) : is connected to the Panel !")
    asyncio.run(ipc_client.request("logUserConnection", user=user))

    # redirect dashboard page
    return redirect('/panel/')


# change code with token
Discordid = {
    "client_id": "1023285147681960069",
    "client_secret": "Sfkq7KeSw-wgNMVidIfETgsFRYB6TK4N",
}


class ExchangeDiscord:
    @staticmethod
    def exchange_code(code: object) -> object:
        data = {
            "client_id": Discordid['client_id'],
            "client_secret": Discordid['client_secret'],
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

        if 'error' in credentials.keys():
            logger.warning(("Problem in exchange code => Return 404 Response !"))
            return None, None

        refresh_token = credentials['refresh_token']
        access_token = credentials['access_token']

        responseUser = requests.get('https://discord.com/api/v10/users/@me', headers={
            'Authorization': 'Bearer %s' % access_token
        })
        responseGuild = requests.get('https://discord.com/api/v10/users/@me/guilds', headers={
            'Authorization': 'Bearer %s' % access_token
        })

        user = responseUser.json()

        guilds_Json = responseGuild.json()

        guilds = []
        for guild in guilds_Json:
            if guild['owner']:
                guild_dico = {"id": guild['id'], "name": guild['name'], "icon": guild['icon'], "owner": guild['owner']}
                guilds.append(guild_dico)

        user['guilds'] = guilds

        logger.info(f"{user['username']} ({user['id']}) : get user sucess !")
        return user, refresh_token

    # change refresh token
    @staticmethod
    def exchange_refresh_token(token):
        data = {
            "client_id": "1023285147681960069",
            "client_secret": "Sfkq7KeSw-wgNMVidIfETgsFRYB6TK4N",
            "grant_type": "refresh_token",
            "refresh_token": token,
            "redirect_uri": "http://127.0.0.1:8000/oauth2/login/redirect",
        }
        headers = {
            'Content_Type': 'application/x-www-form-urlencoded'
        }
        response = requests.post("https://discord.com/api/oauth2/token", data=data, headers=headers)

        credentials = response.json()
        if 'error' in credentials.keys():
            logger.warning(("Problem in exchange Refresh Token !" + str(credentials)))
            return None, token

        refresh_token = credentials['refresh_token']

        access_token = credentials['access_token']

        responseUser = requests.get('https://discord.com/api/v10/users/@me', headers={
            'Authorization': 'Bearer %s' % access_token
        })
        responseGuild = requests.get('https://discord.com/api/v10/users/@me/guilds', headers={
            'Authorization': 'Bearer %s' % access_token
        })

        user = responseUser.json()

        guilds_Json = responseGuild.json()

        guilds = []
        for guild in guilds_Json:
            if guild['owner']:
                guild_dico = {"id": guild['id'], "name": guild['name'], "icon": guild['icon'], "owner": guild['owner']}
                guilds.append(guild_dico)

        user['guilds'] = guilds

        find_token = get_object_or_404(RefreshToken)
        if find_token == Http404:
            RefreshToken.objects.create_token_refresh(user, token)
        else:
            if find_token.token != token:
                find_token.token = token
                find_token.save()

        logger.info(f"{user['username']} ({user['id']}) : refresh sucess !")
        return user, refresh_token


# Verif Discord ans refreshToken
class DiscordVerification:

    @staticmethod
    def check_refresh_token(user, token):
        find_token = get_object_or_404(RefreshToken)
        if find_token == Http404:
            RefreshToken.objects.create_token_refresh(user, token)
        else:
            if find_token.token != token:
                find_token.token = str(token)
                find_token.save()

        return find_token

    @staticmethod
    def check_discord_user(user):
        try:
            discord_tag = '%s#%s' % (user['username'], user['discriminator'])
        except:
            discord_tag = user['discord_tag']
        dico_user = {
            "id": user['id'],
            "discord_tag": discord_tag,
            "avatar": user['avatar'],
            "locale": user['locale'],
            "premium_type": user['premium_type'],
            "username": user['username'],
            "tag": user['discriminator'],
            "mfa_enabled": user['mfa_enabled'],
            "guilds": user['guilds']
        }

        find_user = get_object_or_404(DiscordUser, id=user['id'])

        if find_user == Http404:
            DiscordUser.objects.create_new_discord_user(dico_user)
        else:
            save_user = False
            for field, value in dico_user.items():
                if getattr(find_user, field) != value:
                    save_user = True
                    setattr(find_user, field, value)
            if save_user:
                find_user.save()

        logger.info(f"{user['username']} ({user['id']}) : check user sucess !")

        return dico_user, True


# Admin Session
def delete_all_unexpired_sessions_for_user(user):
    unexpired_sessions = Session.objects.filter(expire_date__gte=timezone.now())
    [
        session.delete() for session in unexpired_sessions
        if str(user.pk) == session.get_decoded().get('_auth_user_id')
    ]


# logout session
def logout(request):
    delete_all_unexpired_sessions_for_user(request.user)

    return redirect("/admin/connexion")
