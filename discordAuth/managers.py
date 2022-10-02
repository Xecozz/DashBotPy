from django.contrib.auth import models


class DiscordUserOauth2Manager(models.UserManager):
    def create_new_discord_user(self, user):
        print('Inside Discord User Manager')
        discord_tag = '%s#%s' % (user['username'], user['discriminator'])
        new_user = self.create(
            id=user['id'],
            avatar=user['avatar'],
            public_flags=user['public_flags'],
            flags=user['flags'],
            locale=user['locale'],
            mfa_enabled=user['mfa_enabled'],
            discord_tag=discord_tag,
            guilds=user['guilds']
        )

        return new_user

    def create_token_refresh(self, user, token):
        new_token = self.create(
            id=user['id'],
            token=token
        )

        return new_token
