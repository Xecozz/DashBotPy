from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from discordAuth.views import get_authenticated_user

def get_user(request, slug):
    user = get_authenticated_user(request)
    if type(user) == HttpResponseRedirect:
        return redirect('/oauth2/login/')

    return render(request, 'Dashboard/index.html', context={'user': user})

def index(request):
    user = get_authenticated_user(request)
    if type(user) == HttpResponseRedirect:
        return redirect('/oauth2/login/')
    guild_array = []
    for guild in user['guilds']:
        if guild['owner']:
            guild_array.append(guild)
    print(guild_array)
    return render(request, 'Dashboard/index.html', context={"user": user, "guilds" : guild_array})