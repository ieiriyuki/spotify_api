#!/usr/bin/env python

import json

import pandas as pd
import requests

from auth import get_client_credentials


def main():
    base_url = "https://api.spotify.com/v1/search"
    token = get_client_credentials()

    headers = {
        "Authorization": "{} {}".format(token["token_type"], token["access_token"])
    }
    params = {"q": "BUMP", "type": "artist", "limit": 10}  # 検索するクエリ  # アーティストだけ取得する
    r = requests.get(base_url, headers=headers, params=params)
    resp = r.json()
    print(json.dumps(resp, indent=2))

    records = []
    for item in resp["artists"]["items"]:
        temp = {
            "id": item["id"],
            "name": item["name"],
            "type": item["type"],
            "genres": item["genres"],
            "popularity": item["popularity"],
            "followers_total": item["followers"]["total"],
            "spotify_url": item["external_urls"]["spotify"],
        }
        records.append(temp)

    pdf = pd.DataFrame.from_records(records)
    print(pdf.head())

    return 1


if __name__ == "__main__":
    main()
