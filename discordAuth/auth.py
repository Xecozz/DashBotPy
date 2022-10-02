from django.contrib.auth.backends import BaseBackend
from .models import DiscordUser, RefreshToken


class DiscordAuthentificationBackend(BaseBackend):
    def authenticate(self, request, user) -> DiscordUser:
        find_user = DiscordUser.objects.filter(id=user['id'])
        if len(find_user) != 0:
            return find_user

        print("User was not found => saving...")
        DiscordUser.objects.create_new_discord_user(user)

        return DiscordUser.objects.filter(id=user['id'])

    def get_user(self, user_id):
        try:
            return DiscordUser.objects.get(pk=user_id)
        except DiscordUser.DoesNotExist:
            return None


class DiscordVerification:

    @staticmethod
    def check_refresh_token(user, token):
        find_token_len = RefreshToken.objects.filter(id=user['id'])

        if len(find_token_len) == 0:
            RefreshToken.objects.create_token_refresh(user, token)
        else:

            find_token = RefreshToken.objects.get(pk=user['id'])
            if find_token.token != token:
                find_token.delete()
                RefreshToken.objects.create_token_refresh(user, token)

        return RefreshToken.objects.get(pk=user['id'])

    @staticmethod
    def check_discord_user(user):
        discord_tag = '%s#%s' % (user['username'], user['discriminator'])
        dico_user = {
            "id": user['id'],
            "discord_tag": discord_tag,
            "avatar": user['avatar'],
            "public_flags": user['public_flags'],
            "flags": user['flags'],
            "locale": user['locale'],
            "mfa_enabled": user['mfa_enabled'],
            "guilds": user['guilds']
        }

        find_user = DiscordUser.objects.get(pk=user['id'])

        dico_find_user = {
            "id": user['id'],
            "discord_tag": discord_tag,
            "avatar": user['avatar'],
            "public_flags": user['public_flags'],
            "flags": user['flags'],
            "locale": user['locale'],
            "mfa_enabled": user['mfa_enabled'],
            "guilds": user['guilds']
        }

        if dico_user != dico_find_user:
            find_user.delete()
            DiscordUser.objects.create_new_discord_user(dico_user)

        return  dico_user
