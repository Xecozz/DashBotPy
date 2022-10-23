import logging


from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from discordAuth.main import check_update

from discordAuth.views import get_authenticated_user, delete_all_unexpired_sessions_for_user

def panel_manager(request, slug):
    # check if user is auth
    user = get_authenticated_user(request)

    if type(user) == HttpResponseRedirect:
        return redirect('/oauth2/login/')

    return render(request, 'panel_manager/panel_manager.html', context={'user': user})


def panel(request):
    user = get_authenticated_user(request)

    if type(user) == HttpResponseRedirect:
        logging.warning('User is not authentificated')
        return redirect('/oauth2/login/')

    user, update = check_update(user)

    if not user:
        logging.warning('Error with check User !')
        return HttpResponseRedirect('/oauth2/login/')


    return render(request, 'panel/panel.html', context={"user": user, "guilds": user['guilds'], 'update': update})


# logout page
def logout_Discord_user(request):
    delete_all_unexpired_sessions_for_user(request.user)
    logging.info(f"{request.user.username} ({request.user.id}) : user logout !")
    return redirect("/")
