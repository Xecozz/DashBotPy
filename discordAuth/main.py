import requests

from .models import DiscordUser


def check_update(user_id):
    token = 'MTAyMzI4NTE0NzY4MTk2MDA2OQ.GCnFcD.OWVtZo99J5D7XKi_IqNNtBwUHWDOV0Y5zSTExs'
    response = requests.get(f'https://discord.com/api/v9/users/{user_id}', headers={
        'Authorization': 'Bearer %s' % token
    })
    response.json()
    print("Json reçu ! ", response)