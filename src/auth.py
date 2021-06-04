#!/usr/bin/env python

from base64 import b64encode
import os

import requests


def get_client_credentials():
    """https://developer.spotify.com/documentation/general/guides/authorization-guide/#client-credentials-flow
    """

    client_id = os.environ['spotify_id']
    client_secret = os.environ['spotify_secret']
    base_url = 'https://accounts.spotify.com/api/token'

    encoded = b64encode('{}:{}'.format(client_id, client_secret).encode())
    auth_value = 'Basic ' + encoded.decode()
    headers = {
        'Authorization': auth_value,
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    params = {'grant_type': 'client_credentials'}
    r = requests.post(base_url, headers=headers, params=params)

    return r.json()


if __name__ == '__main__':
    get_client_credentials()
