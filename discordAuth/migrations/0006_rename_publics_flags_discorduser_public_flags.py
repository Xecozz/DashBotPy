# Generated by Django 4.1.1 on 2022-09-27 19:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('discordAuth', '0005_rename_public_flags_discorduser_publics_flags'),
    ]

    operations = [
        migrations.RenameField(
            model_name='discorduser',
            old_name='publics_flags',
            new_name='public_flags',
        ),
    ]
