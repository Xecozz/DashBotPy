# Generated by Django 4.1.1 on 2022-10-02 11:06

import discordAuth.managers
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discordAuth', '0011_refreshtoken'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='refreshtoken',
            managers=[
                ('objects', discordAuth.managers.DiscordUserOauth2Manager()),
            ],
        ),
        migrations.AlterField(
            model_name='refreshtoken',
            name='token',
            field=models.TextField(),
        ),
    ]
