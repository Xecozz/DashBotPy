# Generated by Django 4.1.1 on 2022-09-27 19:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('discordAuth', '0004_rename_publics_flags_discorduser_public_flags'),
    ]

    operations = [
        migrations.RenameField(
            model_name='discorduser',
            old_name='public_flags',
            new_name='publics_flags',
        ),
    ]
