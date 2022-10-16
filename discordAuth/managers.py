import logging
from datetime import datetime

from django.contrib.auth import models


#backend system
class DiscordUserOauth2Manager(models.UserManager):
    def create_new_discord_user(self, user):
        logging.info(f"{user['username']} ({user['id']}) : Inside Discord User Manager")
        discord_tag = '%s#%s' % (user['username'], user['discriminator'])
        new_user = self.create(
            id=user['id'],
            username = user['username'],
            tag= user['discriminator'],
            avatar=user['avatar'],
            locale=user['locale'],
            premium_type=user['premium_type'],
            mfa_enabled=user['mfa_enabled'],
            discord_tag=discord_tag,
            guilds=user['guilds']
        )

        return new_user

    def create_token_refresh(self, user, token):
        new_token = self.create(
            id=user['id'],
            token=token,
            last_date=datetime.now()

        )
        logging.info(f"{user['username']} ({user['id']}) : Create refresh Token")

        return new_token
