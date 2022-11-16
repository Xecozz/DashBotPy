import asyncio

from discord.ext import ipc

from Dashboard.models import ChannelSetup
from packages.log import LogInit

logger = LogInit("Dashboard.Systems.accueil_manager").logger
ipc_client = ipc.Client(secret_key="pynel")


def annonceSystem(request, slug):
    channelAnnonceSave = False
    annonceSend = False
    message = None
    if request.method == "POST":
        # init

        if request.POST.get("channel_annonce"):
            if request.POST.get("channel") != "None":
                ChannelSetup.objects.update_or_create(guild_id=slug,
                                                      defaults={'channel_annonce': request.POST.get("channel_annonce")})
                channelAnnonceSave = True

        if request.POST.get("message_annonce"):
            AnnonceResult = asyncio.run(
                ipc_client.request("sendAnnonceMessage", guildId=int(slug),
                                   message=request.POST.get("message_annonce")))
            annonceSend = True

            if AnnonceResult['status']:
                logger.info(f"Annonce send !")
                message = request.POST.get("message_annonce")

    try:
        channelAnnonce = ChannelSetup.objects.get(guild_id=slug).channel_annonce
    except:
        channelAnnonce = None

    dico = {"annonceSend": annonceSend, "message": message, "channelAnnonce": channelAnnonce,
            "channelAnnonceSave": channelAnnonceSave}

    return dico


def logsSystem(request, slug):
    channelLogsSave = False

    if request.method == "POST":
        # init
        if request.POST.get("channel_logs"):
            if request.POST.get("channel_logs") != "None":
                ChannelSetup.objects.update_or_create(guild_id=slug,
                                                      defaults={'channel_logs': request.POST.get("channel_logs")})
                channelLogsSave = True

    try:
        channelLogs = ChannelSetup.objects.get(guild_id=slug).channel_logs
    except:
        channelLogs = None

    dico = {"channelLogs": channelLogs, "channelLogsSave": channelLogsSave}

    return dico
