# Generated by Django 4.1.1 on 2022-11-12 16:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Dashboard', '0006_rename_disocrdchannelsetup_discordchannelsetup'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='DiscordChannelSetup',
            new_name='ChannelSetup',
        ),
    ]
