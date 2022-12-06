import asyncio

from Dashboard.Systems.accueil_manager import annonceSystem, logsSystem
from Dashboard.models import ChannelSetup
from discordAuth.models import RefreshToken
from packages.log import LogInit

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect

from discordAuth.update_check import check_update

from discordAuth.views import get_authenticated_user, delete_all_unexpired_sessions_for_user
from discord.ext import ipc

# logger
logger = LogInit("Dashboard.views").logger

ipc_client = ipc.Client(secret_key="pynel")




# index page
def index(request):
    return HttpResponse('Index')


# panel
def panel(request):
    user = get_authenticated_user(request)

    if type(user) == HttpResponseRedirect:
        return redirect('/oauth2/login/')

    user, update = check_update(user)

    if not user:
        return update

    date = RefreshToken.objects.get(id=user['id']).last_date

    return render(request, 'panel/panel.html',
                  context={'user': user, 'guilds': user['guilds'], 'update': update, 'last_date': date})


# acueil page Manage
def accueil(request, slug):
    # check if user is auth
    user = get_authenticated_user(request)

    if type(user) == HttpResponseRedirect:
        return redirect('/oauth2/login/')

    data = asyncio.run(ipc_client.request("getGuildInfo", guildId=int(slug), userId=int(user['id'])))
    if not data['status']:
        return HttpResponse(data['message'])

    dico_annonce = annonceSystem(request, slug)
    dico_logs = logsSystem(request, slug)

    for i in data['guildInfo']['channels_names']:
        # if
        if i['id'] == dico_annonce['channelAnnonce']:
            dico_annonce['channelAnnonce'] = i
        elif i['id'] == dico_logs['channelLogs']:
            dico_logs['channelLogs'] = i

    return render(request, 'panel_manager/accueil.html',
                  context={'guild': data['guildInfo'], 'slug': slug, 'dico_annonce': dico_annonce,
                           'dico_logs': dico_logs})


# manage page Manage
def manage_members(request, slug):
    user = get_authenticated_user(request)

    if type(user) == HttpResponseRedirect:
        return redirect('/oauth2/login/')

    data = asyncio.run(ipc_client.request("getGuildInfo", guildId=int(slug), userId=int(user['id'])))
    if not data['status']:
        return HttpResponse(['message'])

    return render(request, 'panel_manager/manage_members.html',
                  context={'slug': slug, 'infoGuild': data})


# logs page Manage
def logs(request, slug):
    user = get_authenticated_user(request)

    if type(user) == HttpResponseRedirect:
        return redirect('/oauth2/login/')


    data = asyncio.run(ipc_client.request("getGuildInfo", guildId=int(slug), userId=int(user['id'])))
    if not data['status']:
        return HttpResponse(data['message'])

    return render(request, 'panel_manager/logs.html',
                  context={'data': data, 'slug': slug, })


# logout page
def logout_Discord_user(request):
    delete_all_unexpired_sessions_for_user(request.user)
    logger.info(f"{request.user.username} ({request.user.id}) : user logout !")
    return redirect("/")
