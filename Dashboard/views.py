import asyncio

from discordAuth.models import RefreshToken
from packages.log import LogInit

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect

from discordAuth.main import check_update

from discordAuth.views import get_authenticated_user, delete_all_unexpired_sessions_for_user
from discord.ext import ipc

# logger
logger = LogInit("Dashboard.views").logger

ipc_client = ipc.Client(secret_key="pynel")


def basicCheck(request):
    user = get_authenticated_user(request)

    if type(user) == HttpResponseRedirect:
        return redirect('/oauth2/login/')

    return user


# index page
def index(request):
    return HttpResponse('Index')


# panel
def panel(request):
    user = basicCheck(request)

    user, update = check_update(user)

    if not user:
        return update

    date = RefreshToken.objects.get(id=user['id']).last_date

    return render(request, 'panel/panel.html',
                  context={'user': user, 'guilds': user['guilds'], 'update': update, 'last_date': date})


# acueil page Manage
def accueil(request, slug):
    # check if user is auth
    user = basicCheck(request)

    infoGuild = asyncio.run(ipc_client.request("getGuildInfo", guildId=int(slug), userId=int(user['id'])))
    if not infoGuild['status']:
        return HttpResponse(infoGuild['message'])

    print(infoGuild)

    return render(request, 'panel_manager/accueil.html',
                  context={'guild': infoGuild['guildInfo'], 'slug': slug})


# manage page Manage
def manage_members(request, slug):
    user = basicCheck(request)

    infoGuild = asyncio.run(ipc_client.request("getGuildInfo", guildId=int(slug), userId=int(user['id'])))
    if not infoGuild['status']:
        return HttpResponse(infoGuild['message'])

    return render(request, 'panel_manager/manage_members.html',
                  context={'slug': slug, 'infoGuild': infoGuild})


# logs page Manage
def logs(request, slug):
    user = basicCheck(request)

    infoGuild = asyncio.run(ipc_client.request("getGuildInfo", guildId=int(slug), userId=int(user['id'])))
    if not infoGuild['status']:
        return HttpResponse(infoGuild['message'])

    return render(request, 'panel_manager/logs.html',
                  context={'infoGuild': infoGuild, 'slug': slug, })


# logout page
def logout_Discord_user(request):
    delete_all_unexpired_sessions_for_user(request.user)
    logger.info(f"{request.user.username} ({request.user.id}) : user logout !")
    return redirect("/")
