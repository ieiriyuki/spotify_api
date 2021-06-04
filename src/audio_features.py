#!/usr/bin/env python

import json

import pandas as pd
import requests
import seaborn as sns

from auth import get_client_credentials


def main():
    base_url = "https://api.spotify.com/v1/audio-features"
    token = get_client_credentials()
    track_ids = [
        "1k1zTwX433BlwP6FLOPBpD",  # なないろ
        "3hRRYgBeunE3PTmnzATTS0",  # 天体観測
        "1YqVJ2YSgwxWpfuENocF2t",  # アカシア
    ]

    headers = {
        "Authorization": "{} {}".format(token["token_type"], token["access_token"])
    }
    params = {"ids": ",".join(track_ids)}
    r = requests.get(base_url, headers=headers, params=params)
    resp = r.json()
    print(json.dumps(resp, indent=2))

    records = []
    for item in resp["audio_features"]:
        temp = {
            "danceability": item["danceability"],
            "energy": item["energy"],
            "key": item["key"],
            "loudness": item["loudness"],
            "mode": item["mode"],
            "speechiness": item["speechiness"],
            "acousticness": item["acousticness"],
            "instrumentalness": item["instrumentalness"],
            "liveness": item["liveness"],
            "valence": item["valence"],
            "tempo": item["tempo"],
        }
        records.append(temp)

    df = pd.DataFrame.from_records(
        records, index=["nanairo", "tentaikanskoku", "acacia"]
    )
    print(df.head())

    pg = sns.pairplot(
        df.reset_index(),
        corner=True,
        diag_kind="hist",
        diag_kws={"multiple": "stack"},
        hue="index",
    )
    pg.add_legend()
    pg.savefig("./pairplot.png")

    return 1


if __name__ == "__main__":
    main()
