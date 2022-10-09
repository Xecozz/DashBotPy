from django.contrib.auth.backends import BaseBackend
from django.http import Http404
from django.shortcuts import get_object_or_404

from .models import DiscordUser, RefreshToken


class DiscordAuthentificationBackend(BaseBackend):
    def authenticate(self, request, user) -> DiscordUser:
        find_user = DiscordUser.objects.filter(id=user['id'])
        if len(find_user) != 0:
            return find_user

        print("User was not found => saving...")
        print("test", user)
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
        find_token = get_object_or_404(RefreshToken)
        if find_token == Http404:
            RefreshToken.objects.create_token_refresh(user, token)
        else:
            if find_token.token != token:
                find_token.token = str(token)
                find_token.save()

        return find_token

    @staticmethod
    def check_discord_user(user):
        try:
            discord_tag = '%s#%s' % (user['username'], user['discriminator'])
        except:
            discord_tag = user['discord_tag']
        dico_user = {
            "id": user['id'],
            "discord_tag": discord_tag,
            "avatar": user['avatar'],
            "locale" : user['locale'],
            "premium_type" : user['premium_type'],
            "username" : user['username'],
            "tag" : user['discriminator'],
            "mfa_enabled": user['mfa_enabled'],
            "guilds": user['guilds']
        }

        find_user = get_object_or_404(DiscordUser)

        if find_user == Http404:
            DiscordUser.objects.create_new_discord_user(dico_user)
        else:
            save_user = False
            for field, value in dico_user.items():
                if getattr(find_user, field) != value:
                    save_user = True
                    setattr(find_user, field, value)
            if save_user:
                find_user.save()

        return dico_user
