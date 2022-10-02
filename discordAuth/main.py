from discordAuth.models import RefreshToken
from .views import exchange_refresh_token
from discordAuth.auth import DiscordVerification


def check_update(user):
    code = RefreshToken.objects.get(pk=user['id']).token

    user, refresh_token = exchange_refresh_token(code)
    DiscordVerification.check_refresh_token(user, refresh_token)

    return DiscordVerification.check_discord_user(user)
