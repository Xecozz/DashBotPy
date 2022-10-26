import logging
from datetime import datetime

from django.http import Http404
from django.shortcuts import get_object_or_404

from discordAuth.models import RefreshToken
from packages.log import CustomFormatter
from packages.modules import getDifference
from .views import ExchangeDiscord
from discordAuth.views import DiscordVerification

# logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

ch.setFormatter(CustomFormatter())

logger.addHandler(ch)


# check refreshToken and discord User in db
def check_update(user):
    find_token = get_object_or_404(RefreshToken, pk=user['id'])

    # get dates
    last_date = find_token.last_date.replace(tzinfo=None)
    now_date = datetime.now().replace(tzinfo=None)

    diff = getDifference(last_date, now_date, interval='secs')

    find_token.last_date = now_date
    find_token.save()

    # if refresh page < 1s return
    if diff > 1:
        if find_token != Http404:
            new_user, refresh_token = ExchangeDiscord.exchange_refresh_token(find_token.token)
            DiscordVerification.check_refresh_token(user, refresh_token)
            user = new_user

        return DiscordVerification.check_discord_user(user)

    logger.warning(f"{user['username']} ({user['id']}) NOT check Update !!")
    return user, False
