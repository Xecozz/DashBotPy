from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from discordAuth.views import get_authenticated_user

def dashboard(request):
    user = get_authenticated_user(request)
    if type(user) == HttpResponseRedirect:
        return redirect('/oauth2/login/')
    return render(request, 'Dashboard/dashboard.html', context={'user': user})