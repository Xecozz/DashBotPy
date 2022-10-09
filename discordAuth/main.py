from datetime import datetime

from django.http import Http404
from django.shortcuts import get_object_or_404

from discordAuth.models import RefreshToken
from .modules import getDifference
from .views import exchange_refresh_token
from discordAuth.auth import DiscordVerification


#check refreshToken and discord User in db
def check_update(user):
    find_token = get_object_or_404(RefreshToken, pk=user['id'])

    #get dates
    last_date = find_token.last_date.replace(tzinfo=None)
    now_date = datetime.now().replace(tzinfo=None)

    diff = getDifference(last_date, now_date, interval='secs')

    find_token.last_date = now_date
    find_token.save()

    #if refresh page < 3s return
    if diff > 3:
        if find_token != Http404:
            new_user, refresh_token = exchange_refresh_token(find_token.token)
            DiscordVerification.check_refresh_token(user, refresh_token)
            user = new_user
            print(user)

        return DiscordVerification.check_discord_user(user)
