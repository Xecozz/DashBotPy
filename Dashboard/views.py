import asyncio

from Dashboard.models import ChannelSetup
from discordAuth.models import RefreshToken
from packages.log import LogInit

from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404

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

    # init
    annonceSend = False
    message = None

    data = asyncio.run(ipc_client.request("getGuildInfo", guildId=int(slug), userId=int(user['id'])))
    if not data['status']:
        return HttpResponse(data['message'])



    #Annonce Channel
    if request.method == "POST":
        if request.POST.get("channel"):

            logger.info(request.POST.get("channel"))
            if request.POST.get("channel") != "None":
                ChannelSetup.objects.update_or_create(guild_id=slug,
                                                      defaults={'channel_annonce': request.POST.get("channel")})

        if request.POST.get("message"):
            logger.info(request.POST.get("message"))
            AnnonceResult = asyncio.run(
                ipc_client.request("sendAnnonceMessage", guildId=int(slug), message=request.POST.get("message")))
            annonceSend = True

            if AnnonceResult['status']:
                logger.info(f"Annonce send !")
                message = request.POST.get("message")

    try:
        channelAnnonce = ChannelSetup.objects.get(guild_id=slug).channel_annonce
    except:
        channelAnnonce = None

    for i in data['guildInfo']['channels_names']:
        if i['id'] == channelAnnonce:
            channelAnnonce = i

    return render(request, 'panel_manager/accueil.html',
                  context={'guild': data['guildInfo'], 'slug': slug, 'AnnonceSend': annonceSend, "message": message,
                           "channelAnnonce": channelAnnonce})


# manage page Manage
def manage_members(request, slug):
    user = basicCheck(request)

    data = asyncio.run(ipc_client.request("getGuildInfo", guildId=int(slug), userId=int(user['id'])))
    if not data['status']:
        return HttpResponse(['message'])

    return render(request, 'panel_manager/manage_members.html',
                  context={'slug': slug, 'infoGuild': data})


# logs page Manage
def logs(request, slug):
    user = basicCheck(request)

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
