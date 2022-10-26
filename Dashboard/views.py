import asyncio
import logging

from discordAuth.models import RefreshToken
from packages.log import CustomFormatter
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404

from discordAuth.main import check_update

from discordAuth.views import get_authenticated_user, delete_all_unexpired_sessions_for_user
from discord.ext import ipc

# logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

ch.setFormatter(CustomFormatter())

logger.addHandler(ch)

ipc_client = ipc.Client(secret_key="pynel")


def panel_manager(request, slug):
    # check if user is auth
    user = get_authenticated_user(request)

    if type(user) == HttpResponseRedirect:
        return redirect('/oauth2/login/')

    return render(request, 'panel_manager/panel_manager.html', context={'user': user})


def panel(request):
    user = get_authenticated_user(request)

    if type(user) == HttpResponseRedirect:
        logger.warning('User is not authentificated')
        return redirect('/oauth2/login/')

    user, update = check_update(user)

    if not user:
        logger.warning('Error with check User !')
        return HttpResponseRedirect('/oauth2/login/')

    date = RefreshToken.objects.get(id=user['id']).last_date
    print(date)

    return render(request, 'panel/panel.html',
                  context={"user": user, "guilds": user['guilds'], 'update': update, 'last_date': date})


# logout page
def logout_Discord_user(request):
    delete_all_unexpired_sessions_for_user(request.user)
    logger.info(f"{request.user.username} ({request.user.id}) : user logout !")
    return redirect("/")
