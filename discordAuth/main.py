from datetime import datetime

from discordAuth.models import RefreshToken
from .views import exchange_refresh_token
from discordAuth.auth import DiscordVerification


def check_update(user):
    code = RefreshToken.objects.get(pk=user['id']).token

    new_user, refresh_token = exchange_refresh_token(code)
    DiscordVerification.check_refresh_token(user, refresh_token)

    if new_user is None:
        new_user = user

    return DiscordVerification.check_discord_user(new_user)


