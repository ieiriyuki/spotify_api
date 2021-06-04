#!/usr/bin/env python

import json

import requests

from auth import get_client_credentials


def main():
    base_url = "https://api.spotify.com/v1/tracks"
    token = get_client_credentials()
    track_id_1 = "1k1zTwX433BlwP6FLOPBpD"  # なないろ
    track_id_2 = "3hRRYgBeunE3PTmnzATTS0"  # 天体観測

    headers = {
        "Authorization": "{} {}".format(token["token_type"], token["access_token"])
    }
    params = {"ids": f"{track_id_1},{track_id_2}"}
    r = requests.get(base_url, headers=headers, params=params)
    resp = r.json()
    print(json.dumps(resp, indent=2))

    return 1


if __name__ == "__main__":
    main()
