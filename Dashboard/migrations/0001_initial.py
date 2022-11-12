# Generated by Django 4.1.1 on 2022-11-12 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DiscordChannelSetup',
            fields=[
                ('guild_id', models.IntegerField(primary_key=True, serialize=False)),
                ('channel_annonce', models.IntegerField(null=True)),
                ('channel_logs', models.IntegerField(default=None, null=True)),
                ('channel_bienvenue', models.IntegerField(default=None, null=True)),
            ],
        ),
    ]
