from datetime import datetime

from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404

from discordAuth.models import RefreshToken
from packages.log import LogInit
from packages.modules import getDifference
from .views import ExchangeDiscord
from discordAuth.views import DiscordVerification

# logger
logger = LogInit("discordAuth.main").logger


# check refreshToken and discord User in db
def check_update(user):
    print(user)
    find_token = get_object_or_404(RefreshToken, pk=user['id'])

    # get dates
    last_date = find_token.last_date.replace(tzinfo=None)
    now_date = datetime.now().replace(tzinfo=None)

    diff = getDifference(last_date, now_date, interval='secs')

    find_token.last_date = now_date
    find_token.save()

    # if refresh page < 1s return
    if diff > 300: # 5min
        # refresh token
        if find_token != Http404:
            new_user, refresh_token = ExchangeDiscord.exchange_refresh_token(find_token.token)
            DiscordVerification.check_refresh_token(user, refresh_token)
            user = new_user

        if not user:
            logger.warning('Error with check User !')
            return None, HttpResponseRedirect('/oauth2/login/')
        return DiscordVerification.check_discord_user(user)

    logger.warning(f"{user['username']} ({user['id']}) NOT check Update !!")
    return user, False
