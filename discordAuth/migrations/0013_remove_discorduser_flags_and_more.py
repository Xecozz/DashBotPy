# Generated by Django 4.1.1 on 2022-10-03 19:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('discordAuth', '0012_alter_refreshtoken_managers_alter_refreshtoken_token'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='discorduser',
            name='flags',
        ),
        migrations.RemoveField(
            model_name='discorduser',
            name='public_flags',
        ),
    ]
