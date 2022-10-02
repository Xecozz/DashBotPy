from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from discordAuth.main import check_update
from discordAuth.views import get_authenticated_user, delete_all_unexpired_sessions_for_user


def dashboard(request, slug):
    user = get_authenticated_user(request)
    if type(user) == HttpResponseRedirect:
        return redirect('/oauth2/login/')

    return render(request, 'Dashboard/index.html', context={'user': user})


def index(request):
    user = get_authenticated_user(request)

    if type(user) == HttpResponseRedirect:
        return redirect('/oauth2/login')
    user = check_update(user)

    return render(request, 'Dashboard/index.html', context={"user": user, "guilds": user['guilds']})

def logout_Discord_user(request):
    delete_all_unexpired_sessions_for_user(request.user)
    return redirect("")
